"""
AVCS VIRTUAL COMPANY
Streamlit UI — Operational Decision Dashboard
Version: v0.3.9 — Local Semantic Scope

Purpose:
- Normalize incident language before dispatch.
- Preserve ACTIVE / UNCERTAIN / NEGATIVE / HISTORICAL semantic states.
- Avoid false positives from broad single-word matches.
- Produce a stable event contract for the existing AVCS pipeline.

No external normalizer.py is required.
"""

import os
import re
import sys
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
    AVCS semantic layer.

    Important design rule:
        UNCERTAIN != ABSENT
        HISTORICAL != ACTIVE
        REPORTED != CONFIRMED

    The normalizer therefore keeps semantic evidence instead of silently
    deleting everything that is not an active positive condition.
    """

    # Exact phrases are preferred over dangerous single-word matches.
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

    # Negation must be close to the detected phrase.
    WINDOW_BEFORE = 70
    WINDOW_AFTER = 70

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

        # Event type is selected from active evidence only.
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
        """
        Extract conditions using sentence-local semantic scope.

        Semantic modifiers cannot cross a sentence boundary. A modifier must
        also be close to the detected condition phrase.
        """
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
        # Modifiers are evaluated only within the same sentence and local
        # word scope. Therefore "No injuries." cannot modify "water ingress"
        # in the next sentence.

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

    def _classify(self, window: str) -> str:
        # Historical context has priority over a simple positive mention.
        if self._matches(window, self.HISTORICAL_PATTERNS):
            return "HISTORICAL"

        if self._matches(window, self.NEGATION_PATTERNS):
            return "NEGATIVE"

        if self._matches(window, self.UNCERTAINTY_PATTERNS):
            return "UNCERTAIN"

        if self._matches(window, self.CONFIRMED_PATTERNS):
            return "CONFIRMED"

        if self._matches(window, self.REPORTED_PATTERNS):
            return "REPORTED"

        return "ACTIVE"

    @staticmethod
    def _matches(text: str, patterns: list) -> bool:
        return any(re.search(p, text, flags=re.IGNORECASE) for p in patterns)

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

    def _temporal_context(self, window: str):
        if self._matches(window, self.HISTORICAL_PATTERNS):
            return "PREVIOUS"
        if self._matches(window, self.CONFIRMED_PATTERNS):
            return "CONFIRMED"
        if self._matches(window, self.REPORTED_PATTERNS):
            return "REPORTED"
        return "CURRENT"

    @staticmethod
    def _determine_event_type(conditions: list) -> str:
        if not conditions:
            return "GENERAL"

        # Criticality first; confidence is a secondary discriminator.
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
# STREAMLIT UI
# ===========================================================================

st.set_page_config(
    page_title="AVCS Virtual Company",
    page_icon="🧭",
    layout="wide",
)

st.title("AVCS VIRTUAL COMPANY")
st.caption("Operational Decision Dashboard — v0.3.9 Local Semantic Scope")

normalizer = SemanticEventNormalizer()

if "last_normalized_event" not in st.session_state:
    st.session_state.last_normalized_event = None

if "event_counter" not in st.session_state:
    st.session_state.event_counter = 0

st.markdown(
    """
### Operational Decision Architecture

`INCIDENT → SEMANTIC STATE → DISPATCHER → 7 Dpts. → AGGREGATION → CONFLICT → DECISION → AUTHORITY → EXECUTION → RECORD`
"""
)

with st.sidebar:
    st.header("Event Input")

    incident_description = st.text_area(
        "Incident Description",
        height=180,
        placeholder=(
            "Example: Collision with fishing vessel. "
            "Water ingress suspected."
        ),
    )

    object_name = st.text_input("Object / Vessel", "")
    position = st.text_input("Position", "")
    heading = st.text_input("Heading", "")
    speed = st.text_input("Speed", "")

    process_event = st.button(
        "PROCESS EVENT",
        type="primary",
        use_container_width=True,
    )

    reset_event = st.button(
        "RESET",
        use_container_width=True,
    )

if reset_event:
    st.session_state.last_normalized_event = None
    st.rerun()

# ---------------------------------------------------------------------------
# NORMALIZATION
# ---------------------------------------------------------------------------

if process_event:
    if not incident_description.strip():
        st.warning("Please enter an incident description.")
    else:
        normalized = normalizer.normalize(incident_description)

        st.session_state.event_counter += 1
        event_id = (
            f"EVT-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
            f"-{st.session_state.event_counter:03d}"
        )

        event_data = {
            "event_id": event_id,
            "description": incident_description,
            "object": object_name,
            "position": position,
            "heading": heading,
            "speed": speed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": normalized["event_type"],
            "severity": normalized["severity"],
            "critical_conditions": normalized["critical_conditions"],
            "critical_conditions_count": normalized["critical_conditions_count"],
            "has_critical": normalized["has_critical"],
            "has_high": normalized["has_high"],
            "semantic_summary": normalized["semantic_summary"],
            "status": normalized["status"],
        }

        st.session_state.last_normalized_event = event_data


# ---------------------------------------------------------------------------
# RESULTS
# ---------------------------------------------------------------------------

event = st.session_state.last_normalized_event

if event is None:
    st.info(
        "Enter an incident and select PROCESS EVENT. "
        "The semantic layer will normalize the event before operational dispatch."
    )
else:
    st.success(f"Event normalized: {event['event_id']}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Event Type", event["event_type"])
    col2.metric("Severity", event["severity"])
    col3.metric("Conditions", event["critical_conditions_count"])
    col4.metric(
        "Avg Confidence",
        f"{event['semantic_summary']['average_confidence']:.2f}",
    )

    st.divider()

    tab1, tab2, tab3 = st.tabs(
        ["Semantic State", "Event Contract", "Architecture"]
    )

    with tab1:
        st.subheader("Semantic Conditions")

        if not event["critical_conditions"]:
            st.info("No recognized critical/high operational condition.")
        else:
            for condition in event["critical_conditions"]:
                state = condition["semantic_state"]

                if state == "NEGATIVE":
                    icon = "⚪"
                elif state == "UNCERTAIN":
                    icon = "🟡"
                elif state == "HISTORICAL":
                    icon = "🔵"
                elif state == "REPORTED":
                    icon = "🟠"
                elif state == "CONFIRMED":
                    icon = "🔴"
                else:
                    icon = "🔴"

                st.markdown(
                    f"### {icon} {condition['condition']} — {state}"
                )

                c1, c2, c3 = st.columns(3)
                c1.write(f"**Severity:** {condition['severity']}")
                c2.write(f"**Polarity:** {condition['polarity']}")
                c3.write(f"**Confidence:** {condition['confidence']:.2f}")

                st.write(
                    f"**Context:** {condition['context']}"
                )
                st.write(
                    f"**Temporal:** {condition['temporal_context']}  |  "
                    f"**Negation:** {condition['negation_found']}  |  "
                    f"**Uncertainty:** {condition['uncertainty_found']}"
                )

                st.divider()

    with tab2:
        st.subheader("AVCS Event Contract")
        st.json(event)

    with tab3:
        st.subheader("Operational Architecture")

        st.code(
            """
RAW INCIDENT
      ↓
SEMANTIC EVENT NORMALIZER
      ↓
SEMANTIC STATE
 ACTIVE / UNCERTAIN / NEGATIVE / HISTORICAL / REPORTED / CONFIRMED
      ↓
CRITICAL CONDITION REGISTER
      ↓
AI DISPATCHER
      ↓
LOOKOUT Dpt. | CHARTS Dpt. | GYRO Dpt.
NAVIGATOR Dpt. | COMPASS Dpt. | HELM Dpt. | CAPTAIN Dpt.
      ↓
AGGREGATION
      ↓
DECISION PROPOSAL
      ↓
AUTHORITY BOUNDARY
      ↓
HUMAN AUTHORITY
      ↓
EXECUTION
      ↓
AVCS DECISION RECORD
            """.strip(),
            language="text",
        )

    st.caption(
        "v0.3.9 principle: semantic modifiers are applied locally, "
        "within the same sentence, and cannot cross sentence boundaries."
    )
