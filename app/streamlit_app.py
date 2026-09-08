"""
AVCS VIRTUAL COMPANY
Streamlit UI — Operational Decision Dashboard
Version: v0.4.1 — Full Combat Machine with Welcome Screen
"""

import os
import re
import sys
import json
from datetime import datetime, timezone

import streamlit as st

# ---------------------------------------------------------------------------
# Project path
# ---------------------------------------------------------------------------
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_PATH not in sys.path:
    sys.path.insert(0, ROOT_PATH)


# ---------------------------------------------------------------------------
# Existing AVCS components
# ---------------------------------------------------------------------------
from core.departments import (
    LookoutDepartment,
    ChartsDepartment,
    GyroDepartment,
    NavigatorDepartment,
    CompassDepartment,
    HelmDepartment,
    CaptainDepartment,
)
from core.dispatcher import Dispatcher
from core.aggregation import Aggregator
from core.conflict_detection import ConflictDetector
from core.decision_engine import DecisionEngine
from core.authority_gate import AuthorityGate
from core.state_machine import StateMachine
from core.risk_engine import RiskEngine
from records.incident_registry import IncidentRegistry


# ===========================================================================
# SEMANTIC EVENT NORMALIZER v0.3.9
# ===========================================================================

class SemanticEventNormalizer:
    """
    AVCS semantic layer with local semantic scope.
    """

    CONDITIONS = {
        "FIRE": {
            "severity": "CRITICAL",
            "patterns": [
                r"\bfire\b",
                r"\bflames?\b",
                r"\bflaming\b",
                r"\bignition\b",
                r"\bburning\b",
            ],
        },
        "SMOKE": {
            "severity": "HIGH",
            "patterns": [
                r"\bsmoke\b",
                r"\bfumes?\b",
            ],
        },
        "EVACUATION": {
            "severity": "CRITICAL",
            "patterns": [
                r"\bevacuate\b",
                r"\bevacuation\b",
                r"\bevacuat(?:ing|ed)\b",
                r"\babandon ship\b",
            ],
        },
        "TEMPERATURE": {
            "severity": "HIGH",
            "patterns": [
                r"\boverheat(?:ing)?\b",
                r"\btemperature\s+(?:is\s+)?(?:rising|high|elevated)\b",
                r"\bhigh\s+temperature\b",
                r"\btemperature\s+alarm\b",
            ],
        },
        "OIL_SPILL": {
            "severity": "CRITICAL",
            "patterns": [
                r"\boil spill\b",
                r"\boil leak\b",
                r"\boil leakage\b",
                r"\boil pollution\b",
                r"\bhydrocarbon spill\b",
                r"\bhydrocarbon leak\b",
            ],
        },
        "HULL_BREACH": {
            "severity": "CRITICAL",
            "patterns": [
                r"\bwater ingress\b",
                r"\bhull breach\b",
                r"\bhull damage\b",
                r"\bhull failure\b",
                r"\bflooding\b",
                r"\bflooded\b",
            ],
        },
        "MAN_OVERBOARD": {
            "severity": "CRITICAL",
            "patterns": [
                r"\bman overboard\b",
                r"\bperson overboard\b",
                r"\bperson in the water\b",
                r"\bMOB\b",
            ],
        },
        "GAS_LEAK": {
            "severity": "CRITICAL",
            "patterns": [
                r"\bgas leak\b",
                r"\bgas leakage\b",
                r"\bmethane leak\b",
                r"\btoxic gas\b",
            ],
        },
        "DRONE": {
            "severity": "HIGH",
            "patterns": [
                r"\bdrone\b",
                r"\bUAV\b",
                r"\bunidentified drone\b",
            ],
        },
        "COLLISION": {
            "severity": "CRITICAL",
            "patterns": [
                r"\bcollision\b",
                r"\bcollided\b",
                r"\bimpact with\b",
                r"\bstruck by\b",
                r"\bstruck\b",
            ],
        },
        "EXPLOSION": {
            "severity": "CRITICAL",
            "patterns": [
                r"\bexplosion\b",
                r"\bexploded\b",
                r"\bblast\b",
            ],
        },
    }

    NEGATION_PATTERNS = [
        r"\bno\b",
        r"\bnot\b",
        r"\bwithout\b",
        r"\bnever\b",
        r"\bruled\s+out\b",
        r"\bexcluded\b",
        r"\babsent\b",
        r"\bno\s+evidence\s+of\b",
        r"\bnot\s+detected\b",
        r"\bwas\s+not\s+detected\b",
    ]

    UNCERTAINTY_PATTERNS = [
        r"\bsuspected\b",
        r"\bsuspect\b",
        r"\bpossible\b",
        r"\bpossibly\b",
        r"\bprobable\b",
        r"\bprobably\b",
        r"\bmaybe\b",
        r"\bpotential\b",
        r"\bpotentially\b",
        r"\bappears?\b",
        r"\bseems?\b",
        r"\bindicates?\b",
        r"\bsuggests?\b",
    ]

    HISTORICAL_PATTERNS = [
        r"\bprevious\b",
        r"\bprior\b",
        r"\bhistorical\b",
        r"\bearlier\b",
        r"\blast\s+shift\b",
        r"\blast\s+week\b",
        r"\byesterday\b",
    ]

    REPORTED_PATTERNS = [
        r"\breported\b",
        r"\breports?\b",
        r"\bstated\b",
        r"\baccording\s+to\b",
    ]

    CONFIRMED_PATTERNS = [
        r"\bconfirmed\b",
        r"\bverified\b",
        r"\bvalidated\b",
    ]

    def normalize(self, text: str) -> dict:
        text = (text or "").strip()

        if not text:
            return {
                "critical_conditions": [],
                "critical_conditions_count": 0,
                "event_type": "GENERAL",
                "severity": "LOW",
                "has_critical": False,
                "has_high": False,
                "semantic_summary": {
                    "total_conditions": 0,
                    "active_conditions": 0,
                    "uncertain_conditions": 0,
                    "negative_conditions": 0,
                    "historical_conditions": 0,
                    "reported_conditions": 0,
                    "confirmed_conditions": 0,
                    "average_confidence": 0.0,
                },
                "status": "NORMALIZED",
            }

        conditions = self._extract(text)
        active = [
            c for c in conditions
            if c["semantic_state"] in ("ACTIVE", "UNCERTAIN", "REPORTED", "CONFIRMED")
        ]

        event_type = self._determine_event_type(active)
        severity = self._determine_overall_severity(active)

        return {
            "critical_conditions": conditions,
            "critical_conditions_count": len(conditions),
            "event_type": event_type,
            "severity": severity,
            "has_critical": any(
                c["severity"] == "CRITICAL" and c["semantic_state"] != "NEGATIVE"
                for c in active
            ),
            "has_high": any(
                c["severity"] == "HIGH" and c["semantic_state"] != "NEGATIVE"
                for c in active
            ),
            "semantic_summary": self._summary(conditions),
            "status": "NORMALIZED",
        }

    def _extract(self, text: str) -> list:
        found = []
        sentence_spans = list(
            re.finditer(r"[^.!?]+(?:[.!?]+|$)", text, flags=re.DOTALL)
        )

        for condition_type, config in self.CONDITIONS.items():
            best = None

            for pattern in config["patterns"]:
                match = re.search(pattern, text, flags=re.IGNORECASE)
                if not match:
                    continue

                sentence = self._sentence_for_position(
                    text, match.start(), sentence_spans
                )
                sentence_start = sentence["start"]
                sentence_text = sentence["text"]

                local_position = match.start() - sentence_start
                local_end = match.end() - sentence_start

                before = sentence_text[:local_position]
                after = sentence_text[local_end:]

                semantic_state = self._classify_local(
                    before=before,
                    after=after,
                )

                context_start = max(0, local_position - 70)
                context_end = min(len(sentence_text), local_end + 70)

                candidate = {
                    "condition": condition_type,
                    "severity": config["severity"],
                    "keyword": match.group(0),
                    "context": sentence_text[context_start:context_end].strip(),
                    "semantic_state": semantic_state,
                    "polarity": self._polarity(semantic_state),
                    "confidence": self._confidence(semantic_state),
                    "uncertainty": (
                        "HIGH" if semantic_state == "UNCERTAIN" else None
                    ),
                    "negation_found": semantic_state == "NEGATIVE",
                    "uncertainty_found": semantic_state == "UNCERTAIN",
                    "temporal_context": self._temporal_context_local(
                        before, after
                    ),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "source": "INCIDENT_INPUT",
                    "status": (
                        "ACTIVE"
                        if semantic_state not in ("NEGATIVE", "HISTORICAL")
                        else "EXCLUDED"
                    ),
                }

                if best is None or self._state_rank(
                    semantic_state
                ) > self._state_rank(best["semantic_state"]):
                    best = candidate

            if best:
                found.append(best)

        return found

    @staticmethod
    def _sentence_for_position(text: str, position: int, spans: list) -> dict:
        for span in spans:
            if span.start() <= position < span.end():
                return {
                    "start": span.start(),
                    "end": span.end(),
                    "text": span.group(0),
                }
        return {"start": 0, "end": len(text), "text": text}

    @staticmethod
    def _local_modifier_before(
        before: str, patterns: list, max_words: int = 7
    ) -> bool:
        words = re.findall(r"\b[\w'-]+\b", before.lower())
        tail = " ".join(words[-max_words:])
        return any(
            re.search(pattern, tail, flags=re.IGNORECASE)
            for pattern in patterns
        )

    @staticmethod
    def _local_modifier_after(
        after: str, patterns: list, max_words: int = 7
    ) -> bool:
        words = re.findall(r"\b[\w'-]+\b", after.lower())
        head = " ".join(words[:max_words])
        return any(
            re.search(pattern, head, flags=re.IGNORECASE)
            for pattern in patterns
        )

    def _classify_local(self, before: str, after: str) -> str:
        if self._local_modifier_before(
            before, self.HISTORICAL_PATTERNS, max_words=7
        ):
            return "HISTORICAL"

        if self._local_modifier_before(
            before, self.NEGATION_PATTERNS, max_words=7
        ):
            return "NEGATIVE"

        if (
            self._local_modifier_before(
                before, self.UNCERTAINTY_PATTERNS, max_words=7
            )
            or self._local_modifier_after(
                after, self.UNCERTAINTY_PATTERNS, max_words=7
            )
        ):
            return "UNCERTAIN"

        if (
            self._local_modifier_before(
                before, self.CONFIRMED_PATTERNS, max_words=7
            )
            or self._local_modifier_after(
                after, self.CONFIRMED_PATTERNS, max_words=7
            )
        ):
            return "CONFIRMED"

        if (
            self._local_modifier_before(
                before, self.REPORTED_PATTERNS, max_words=7
            )
            or self._local_modifier_after(
                after, self.REPORTED_PATTERNS, max_words=7
            )
        ):
            return "REPORTED"

        return "ACTIVE"

    @staticmethod
    def _temporal_context_local(before: str, after: str):
        if SemanticEventNormalizer._local_modifier_before(
            before, SemanticEventNormalizer.HISTORICAL_PATTERNS, max_words=7
        ):
            return "PREVIOUS"

        if (
            SemanticEventNormalizer._local_modifier_before(
                before, SemanticEventNormalizer.CONFIRMED_PATTERNS, max_words=7
            )
            or SemanticEventNormalizer._local_modifier_after(
                after, SemanticEventNormalizer.CONFIRMED_PATTERNS, max_words=7
            )
        ):
            return "CONFIRMED"

        if (
            SemanticEventNormalizer._local_modifier_before(
                before, SemanticEventNormalizer.REPORTED_PATTERNS, max_words=7
            )
            or SemanticEventNormalizer._local_modifier_after(
                after, SemanticEventNormalizer.REPORTED_PATTERNS, max_words=7
            )
        ):
            return "REPORTED"

        return "CURRENT"

    @staticmethod
    def _state_rank(state: str) -> int:
        return {
            "NEGATIVE": 0,
            "HISTORICAL": 1,
            "REPORTED": 2,
            "UNCERTAIN": 3,
            "ACTIVE": 4,
            "CONFIRMED": 5,
        }.get(state, 0)

    @staticmethod
    def _polarity(state: str) -> str:
        if state == "NEGATIVE":
            return "NEGATIVE"
        if state == "UNCERTAIN":
            return "NEUTRAL"
        return "POSITIVE"

    @staticmethod
    def _confidence(state: str) -> float:
        return {
            "NEGATIVE": 0.95,
            "HISTORICAL": 0.90,
            "REPORTED": 0.70,
            "UNCERTAIN": 0.60,
            "ACTIVE": 0.80,
            "CONFIRMED": 0.95,
        }.get(state, 0.50)

    @staticmethod
    def _determine_event_type(conditions: list) -> str:
        if not conditions:
            return "GENERAL"

        critical = [c for c in conditions if c["severity"] == "CRITICAL"]
        if critical:
            critical.sort(
                key=lambda c: (
                    SemanticEventNormalizer._state_rank(c["semantic_state"]),
                    c["confidence"],
                ),
                reverse=True,
            )
            return critical[0]["condition"]

        high = [c for c in conditions if c["severity"] == "HIGH"]
        if high:
            high.sort(key=lambda c: c["confidence"], reverse=True)
            return high[0]["condition"]

        return conditions[0]["condition"]

    @staticmethod
    def _determine_overall_severity(conditions: list) -> str:
        if any(c["severity"] == "CRITICAL" for c in conditions):
            return "CRITICAL"
        if any(c["severity"] == "HIGH" for c in conditions):
            return "HIGH"
        return "LOW"

    @staticmethod
    def _summary(conditions: list) -> dict:
        if not conditions:
            return {
                "total_conditions": 0,
                "active_conditions": 0,
                "uncertain_conditions": 0,
                "negative_conditions": 0,
                "historical_conditions": 0,
                "reported_conditions": 0,
                "confirmed_conditions": 0,
                "average_confidence": 0.0,
            }

        states = [c["semantic_state"] for c in conditions]
        return {
            "total_conditions": len(conditions),
            "active_conditions": states.count("ACTIVE"),
            "uncertain_conditions": states.count("UNCERTAIN"),
            "negative_conditions": states.count("NEGATIVE"),
            "historical_conditions": states.count("HISTORICAL"),
            "reported_conditions": states.count("REPORTED"),
            "confirmed_conditions": states.count("CONFIRMED"),
            "average_confidence": round(
                sum(c["confidence"] for c in conditions) / len(conditions), 3
            ),
        }


# ===========================================================================
# STREAMLIT UI — FULL COMBAT MACHINE v0.4.1
# ===========================================================================

st.set_page_config(
    page_title="AVCS Virtual Company",
    page_icon="🧭",
    layout="wide",
)

# ---------------------------------------------------------------------------
# WELCOME SCREEN
# ---------------------------------------------------------------------------

if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False

if not st.session_state.welcome_shown:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            image_path = os.path.join(ROOT_PATH, "app", "north_is_not_negotiable.png")
            if os.path.exists(image_path):
                st.image(image_path, use_container_width=True)
            else:
                st.warning("North image not found. Please check the file path.")
        except Exception as e:
            st.error(f"Error loading image: {e}")

        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; color: #8a8a8a; font-family: 'Courier New', monospace;">
                <p style="font-size: 18px; letter-spacing: 2px;">
                    STRUCTURAL INTEGRITY FOR DECISIONS UNDER PRESSURE
                </p>
                <p style="font-size: 14px; color: #555;">
                    AVCS — Adaptive Vector Control System
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("▸ ENTER COMMAND CENTER", use_container_width=True, type="primary"):
            st.session_state.welcome_shown = True
            st.rerun()

    st.stop()

# ===========================================================================
# MAIN APPLICATION
# ===========================================================================

st.title("🧭 AVCS VIRTUAL COMPANY")
st.caption("AI-Driven Operational Decision Architecture — v0.4.1 Full Combat Machine")

# Инициализация сессии
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.event_id = None
    st.session_state.current_step = "input"
    st.session_state.event_data = None
    st.session_state.dispatcher_results = None
    st.session_state.department_results = None
    st.session_state.aggregated_state = None
    st.session_state.conflict_result = None
    st.session_state.decision_proposal = None
    st.session_state.authority_state = None
    st.session_state.authorized = None
    st.session_state.incident_text = ""
    st.session_state.object_type = ""
    st.session_state.position = ""
    st.session_state.heading = 0
    st.session_state.speed = 0

normalizer = SemanticEventNormalizer()

# --- Sidebar ---
with st.sidebar:
    try:
        st.image("app/logo.png", width=200)
    except:
        st.markdown("### 🧭 AVCS")
    
    st.divider()
    st.header("System Status")
    if st.session_state.get("event_id"):
        st.info(f"Event: {st.session_state.event_id}")
    else:
        st.info("No active event")
    st.write(f"Step: {st.session_state.current_step}")
    st.divider()
    st.header("Architecture")
    st.caption("INCIDENT → SEMANTIC STATE → DISPATCHER → 7 Dpts. → AGGREGATION → CONFLICT → DECISION → AUTHORITY → EXECUTION → RECORD")
    st.divider()
    st.caption("Version: 0.4.1")

    if st.button("🔄 Reset Event", use_container_width=True):
        for key in ["event_id", "event_data", "dispatcher_results", "department_results", 
                    "aggregated_state", "conflict_result", "decision_proposal", 
                    "authority_state", "authorized", "current_step"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.current_step = "input"
        st.session_state.incident_text = ""
        st.session_state.object_type = ""
        st.session_state.position = ""
        st.session_state.heading = 0
        st.session_state.speed = 0
        st.rerun()

# --- Основные вкладки ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📥 Incident Input",
    "⚙️ Processing",
    "📋 Decision",
    "📊 Record",
    "📋 Incident Registry"
])

# --- TAB 1: INCIDENT INPUT ---
with tab1:
    st.header("Incident Input")
    st.caption("Describe any incident — the system will classify and process it automatically.")

    incident_description = st.text_area(
        "Incident Description",
        value=st.session_state.incident_text,
        height=150,
        placeholder="Describe the incident in detail..."
    )

    col1, col2 = st.columns(2)
    with col1:
        object_type = st.text_input("Object / Vessel (optional)", value=st.session_state.object_type)
        position = st.text_input("Position (optional)", value=st.session_state.position)
    with col2:
        heading = st.number_input("Heading (optional)", min_value=0, max_value=360, value=st.session_state.heading)
        speed = st.number_input("Speed (optional)", min_value=0, max_value=100, value=st.session_state.speed)

    if st.button("🚀 Process Incident", type="primary"):
        if not incident_description.strip():
            st.error("Please describe the incident.")
        else:
            st.session_state.incident_text = incident_description
            st.session_state.object_type = object_type
            st.session_state.position = position
            st.session_state.heading = heading
            st.session_state.speed = speed

            normalized = normalizer.normalize(incident_description)

            registry = IncidentRegistry()
            event_id = registry.generate_event_id()

            event_data = {
                "event_id": event_id,
                "description": incident_description,
                "object": object_type if object_type else "Unknown",
                "position": position if position else "Unknown",
                "heading": heading,
                "speed": speed,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "escalate": True,
                "event_type": normalized["event_type"],
                "severity": normalized["severity"],
                "critical_conditions": normalized["critical_conditions"],
                "critical_conditions_count": normalized["critical_conditions_count"],
                "has_critical": normalized["has_critical"],
                "has_high": normalized["has_high"],
                "semantic_summary": normalized["semantic_summary"],
                "status": normalized["status"],
            }

            registry.add_incident(event_data)

            st.session_state.event_data = event_data
            st.session_state.event_id = event_data["event_id"]
            st.session_state.current_step = "processing"
            st.rerun()

    if st.session_state.get("event_id"):
        st.success(f"Event created: {st.session_state.event_id}")
        if st.session_state.get("event_data") and "critical_conditions" in st.session_state.get("event_data", {}):
            with st.expander("📋 Critical Conditions Extracted"):
                st.json(st.session_state.event_data["critical_conditions"])

# --- TAB 2: PROCESSING ---
with tab2:
    st.header("Processing Pipeline")

    if st.session_state.current_step == "processing" and st.session_state.event_data:
        with st.spinner("Processing incident..."):
            lookout = LookoutDepartment()
            charts = ChartsDepartment()
            gyro = GyroDepartment()
            navigator = NavigatorDepartment()
            compass = CompassDepartment()
            helm = HelmDepartment()
            captain = CaptainDepartment()

            dispatcher = Dispatcher()
            dispatcher.register_department(lookout)
            dispatcher.register_department(charts)
            dispatcher.register_department(gyro)
            dispatcher.register_department(navigator)
            dispatcher.register_department(compass)
            dispatcher.register_department(helm)
            dispatcher.register_department(captain)

            aggregator = Aggregator()
            conflict_detector = ConflictDetector()
            decision_engine = DecisionEngine()
            authority_gate = AuthorityGate()
            state_machine = StateMachine()
            risk_engine = RiskEngine()

            event_data = st.session_state.event_data.copy()
            event_data["situation"] = event_data.get("description", "Incident detected")
            event_data["time_to_event"] = 5
            event_data["action"] = "Analyze and respond"
            event_data["authorized"] = False
            event_data["decision_proposal"] = "Awaiting assessment"
            event_data["evidence"] = [f"Event type: {event_data.get('event_type', 'UNKNOWN')}"]
            event_data["current_heading"] = event_data.get("heading", 0)
            event_data["current_speed"] = event_data.get("speed", 0)
            event_data["threat_heading"] = 0
            event_data["threat_speed"] = 0
            event_data["separation_required"] = 0.5

            state_machine.start(st.session_state.event_id)
            state_machine.dispatch()
            dispatcher_results = dispatcher.process_incoming_event(event_data)

            state_machine.process()
            task_packets = dispatcher_results.get("task_packets", [])
            department_results = {}
            for packet in task_packets:
                dept_name = packet["department"]
                dept_data = packet["data"]
                if dept_name == "LOOKOUT Dpt.":
                    result = lookout.process(dept_data)
                elif dept_name == "CHARTS Dpt.":
                    result = charts.process(dept_data)
                elif dept_name == "GYRO Dpt.":
                    result = gyro.process(dept_data)
                elif dept_name == "NAVIGATOR Dpt.":
                    result = navigator.process(dept_data)
                elif dept_name == "COMPASS Dpt.":
                    result = compass.process(dept_data)
                elif dept_name == "HELM Dpt.":
                    result = helm.process(dept_data)
                elif dept_name == "CAPTAIN Dpt.":
                    result = captain.process(dept_data)
                else:
                    result = {"error": f"Unknown department: {dept_name}"}
                department_results[dept_name] = result

            state_machine.aggregate()
            aggregated_state = aggregator.aggregate(department_results, st.session_state.event_id)

            risk_assessment = risk_engine.evaluate_risk(event_data.get("critical_conditions", []))
            aggregated_state["risk_assessment"] = risk_assessment

            state_machine.detect_conflicts()
            conflict_result = conflict_detector.detect(aggregated_state)

            state_machine.formulate_decision()
            decision_proposal = decision_engine.formulate(aggregated_state, conflict_result)
            decision_proposal["risk_assessment"] = risk_assessment

            state_machine.wait_for_authority()
            authority_state = authority_gate.present_decision(decision_proposal)

            st.session_state.dispatcher_results = dispatcher_results
            st.session_state.department_results = department_results
            st.session_state.aggregated_state = aggregated_state
            st.session_state.conflict_result = conflict_result
            st.session_state.decision_proposal = decision_proposal
            st.session_state.authority_state = authority_state
            st.session_state.current_step = "authority"

            registry = IncidentRegistry()
            registry.add_incident({
                **event_data,
                "decision_proposal": decision_proposal,
                "authorized": False,
                "status": "AWAITING_AUTHORITY"
            })

            st.rerun()

    if st.session_state.get("department_results"):
        st.subheader("Department Assessments")
        for dept, result in st.session_state.department_results.items():
            with st.expander(f"📋 {dept}"):
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.json(result)

    if st.session_state.get("aggregated_state"):
        st.subheader("📊 Aggregated State")
        st.json(st.session_state.aggregated_state)

        if "risk_assessment" in st.session_state.aggregated_state:
            st.subheader("⚠️ Risk Assessment")
            risk_data = st.session_state.aggregated_state["risk_assessment"]
            if risk_data.get("overall_risk") == "CRITICAL":
                st.error(f"🚨 CRITICAL RISK: {risk_data.get('risk_count', 0)} risks identified")
            elif risk_data.get("overall_risk") == "HIGH":
                st.warning(f"⚠️ HIGH RISK: {risk_data.get('risk_count', 0)} risks identified")
            else:
                st.success(f"✅ LOW RISK: {risk_data.get('risk_count', 0)} risks identified")
            st.json(risk_data)

    if st.session_state.get("conflict_result"):
        st.subheader("⚠️ Conflict Detection")
        if st.session_state.conflict_result.get("has_conflicts"):
            st.warning("Conflicts detected!")
        else:
            st.success("No conflicts detected")
        st.json(st.session_state.conflict_result)

# --- TAB 3: DECISION ---
with tab3:
    st.header("Decision Authority")

    if st.session_state.get("decision_proposal"):
        st.subheader("Decision Proposal")
        st.json(st.session_state.decision_proposal)

    if st.session_state.get("authority_state"):
        st.subheader("Authority Gate")
        st.json(st.session_state.authority_state)

        if st.session_state.authority_state.get("status") == "PENDING":
            st.divider()
            st.markdown("### 🔐 Human Authorization Required")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Approve", type="primary"):
                    st.session_state.authorized = True
                    st.session_state.current_step = "executing"
                    registry = IncidentRegistry()
                    registry.update_incident(st.session_state.event_id, {
                        "authorized": True,
                        "status": "AUTHORIZED"
                    })
                    st.rerun()
            with col2:
                if st.button("❌ Reject", type="secondary"):
                    st.session_state.authorized = False
                    st.session_state.current_step = "completed"
                    registry = IncidentRegistry()
                    registry.update_incident(st.session_state.event_id, {
                        "authorized": False,
                        "status": "REJECTED"
                    })
                    st.rerun()

        if st.session_state.get("authorized") is True:
            st.success("✅ Decision Authorized")
            st.session_state.current_step = "completed"
        elif st.session_state.get("authorized") is False:
            st.error("❌ Decision Rejected")

# --- TAB 4: RECORD ---
with tab4:
    st.header("AVCS Decision Record")

    if st.session_state.current_step == "completed" or st.session_state.get("authorized") is not None:
        if st.session_state.get("authorized"):
            st.success("Decision Cycle Completed — Authorized")
        else:
            st.info("Decision Cycle Completed — Rejected")

        record = {
            "event_id": st.session_state.event_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "COMPLETED",
            "authorized": st.session_state.authorized,
            "decision_proposal": st.session_state.decision_proposal,
            "authority_state": st.session_state.authority_state,
            "aggregated_state": st.session_state.aggregated_state,
            "conflict_result": st.session_state.conflict_result
        }

        st.json(record)

        st.download_button(
            label="📥 Download AVCS Record",
            data=json.dumps(record, indent=2),
            file_name=f"AVCS_RECORD_{st.session_state.event_id}.json",
            mime="application/json"
        )
    else:
        st.info("Complete the decision cycle to generate AVCS Record")

# --- TAB 5: INCIDENT REGISTRY ---
with tab5:
    st.header("📋 Incident Registry")
    st.caption("История всех обработанных инцидентов. Автоочистка >30 дней.")
    
    registry = IncidentRegistry()
    incidents = registry.get_all_incidents()
    stats = registry.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Incidents", stats["total"])
    with col2:
        st.metric("Event Types", len(stats["by_type"]))
    with col3:
        st.metric("Critical", stats["by_severity"].get("CRITICAL", 0))
    with col4:
        st.metric("Authorized", stats["by_status"].get("AUTHORIZED", 0))
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        filter_type = st.selectbox("Filter by Event Type", ["All"] + list(stats["by_type"].keys()))
    with col2:
        filter_status = st.selectbox("Filter by Status", ["All"] + list(stats["by_status"].keys()))
    
    filtered_incidents = incidents
    if filter_type != "All":
        filtered_incidents = [i for i in filtered_incidents if i.get("event_type") == filter_type]
    if filter_status != "All":
        filtered_incidents = [i for i in filtered_incidents if i.get("status") == filter_status]
    
    if not filtered_incidents:
        st.info("No incidents found.")
    else:
        st.write(f"Showing {len(filtered_incidents)} of {len(incidents)} incidents")
        
        for incident in reversed(filtered_incidents[-50:]):
            with st.expander(f"{incident['event_id']} — {incident['event_type']} ({incident['status']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Description:** {incident.get('description', 'N/A')}")
                    st.write(f"**Severity:** {incident.get('severity', 'UNKNOWN')}")
                    st.write(f"**Authorized:** {incident.get('authorized', False)}")
                with col2:
                    st.write(f"**Timestamp:** {incident.get('timestamp', 'N/A')}")
                    if incident.get("critical_conditions"):
                        st.write("**Critical Conditions:**")
                        for cond in incident.get("critical_conditions", []):
                            st.write(f"- {cond.get('condition')} ({cond.get('severity')})")
                
                if st.button(f"View Record", key=f"view_{incident['event_id']}"):
                    st.json(incident.get("record", {}))
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Old Records (>30 days)"):
            removed = registry.clear_old_records(30)
            if removed > 0:
                st.success(f"Removed {removed} old records.")
            else:
                st.info("No records older than 30 days.")
            st.rerun()
    
