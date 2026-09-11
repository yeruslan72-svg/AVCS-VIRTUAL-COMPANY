"""
AVCS VIRTUAL COMPANY
Streamlit UI — Operational Decision Dashboard
Version: v0.5.2 — Constitution-Aligned Sequential 

ARCHITECTURE:
INCIDENT → SEMANTIC STATE → SEQUENTIAL EXECUTOR → 7 Dpts. (INS-A) →
AGGREGATION → CONFLICT → DECISION → AUTHORITY → RECORD
"""

import os
import re
import sys
import json
from datetime import datetime, timezone

import streamlit as st

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_PATH not in sys.path:
    sys.path.insert(0, ROOT_PATH)

from core.departments import (
    LookoutDepartment,
    ChartsDepartment,
    GyroDepartment,
    NavigatorDepartment,
    CompassDepartment,
    HelmDepartment,
    CaptainDepartment,
)
from core.sequential_executor import SequentialExecutor
from core.aggregation import Aggregator
from core.conflict_detection import ConflictDetector
from core.decision_engine import DecisionEngine
from core.authority_gate import AuthorityGate
from core.state_machine import StateMachine
from records.incident_registry import IncidentRegistry


# ===========================================================================
# SEMANTIC EVENT NORMALIZER v0.3.9
# ===========================================================================

class SemanticEventNormalizer:
    """
    AVCS semantic layer with local semantic scope.
    """

    CONDITIONS = {
        "FIRE": {"severity": "CRITICAL", "patterns": [r"\bfire\b", r"\bflames?\b", r"\bflaming\b", r"\bignition\b", r"\bburning\b"]},
        "FIRE_EXTINGUISHED": {"severity": "MEDIUM", "patterns": [r"\bfire\s+under\s+control\b", r"\bfire\s+extinguished\b", r"\bfire\s+out\b"]},
        "SMOKE": {"severity": "HIGH", "patterns": [r"\bsmoke\b", r"\bfumes?\b"]},
        "EVACUATION": {"severity": "CRITICAL", "patterns": [r"\bevacuate\b", r"\bevacuation\b", r"\bevacuat(?:ing|ed)\b", r"\babandon ship\b"]},
        "ABANDONMENT": {"severity": "CRITICAL", "patterns": [r"\babandon\s+ship\b", r"\babandoning\b", r"\btaking\s+to\s+lifeboats\b"]},
        "TEMPERATURE": {"severity": "HIGH", "patterns": [r"\boverheat(?:ing)?\b", r"\btemperature\s+(?:is\s+)?(?:rising|high|elevated)\b", r"\bhigh\s+temperature\b", r"\btemperature\s+alarm\b"]},
        "OIL_SPILL": {"severity": "CRITICAL", "patterns": [r"\boil spill\b", r"\boil leak\b", r"\boil leakage\b", r"\boil pollution\b", r"\bhydrocarbon spill\b", r"\bhydrocarbon leak\b"]},
        "POLLUTION": {"severity": "CRITICAL", "patterns": [r"\bpollution\b", r"\benvironmental\b", r"\bcontamination\b", r"\btoxic release\b"]},
        "HULL_BREACH": {"severity": "CRITICAL", "patterns": [r"\bwater ingress\b", r"\bhull breach\b", r"\bhull damage\b", r"\bhull failure\b", r"\bflooding\b", r"\bflooded\b"]},
        "FLOODING": {"severity": "CRITICAL", "patterns": [r"\bflooding\b", r"\bwater ingress\b", r"\buncontrolled water\b", r"\bprogressive flooding\b"]},
        "MAN_OVERBOARD": {"severity": "CRITICAL", "patterns": [r"\bman overboard\b", r"\bperson overboard\b", r"\bperson in the water\b", r"\bMOB\b"]},
        "GAS_LEAK": {"severity": "CRITICAL", "patterns": [r"\bgas leak\b", r"\bgas leakage\b", r"\bmethane leak\b", r"\btoxic gas\b"]},
        "DRONE": {"severity": "HIGH", "patterns": [r"\bdrone\b", r"\bUAV\b", r"\bunidentified drone\b"]},
        "MARITIME_DRONE": {"severity": "HIGH", "patterns": [r"\bmaritime\s+drone\b", r"\bsea\s+drone\b", r"\bunmanned\s+vessel\b", r"\busv\b", r"\bunmanned\s+surface\s+vessel\b", r"\bautonomous\s+vessel\b"]},
        "COLLISION": {"severity": "CRITICAL", "patterns": [r"\bcollision\b", r"\bcollided\b", r"\bimpact with\b", r"\bstruck by\b", r"\bstruck\b"]},
        "COLLISION_RISK": {"severity": "CRITICAL", "patterns": [r"\bcollision\s+risk\b", r"\brisk\s+of\s+collision\b", r"\bimminent\s+collision\b", r"\bon\s+collision\s+course\b", r"\bconverging\s+course\b", r"\bapproaching\s+vessel\b", r"\bclosing\s+speed\b"]},
        "GROUNDING": {"severity": "CRITICAL", "patterns": [r"\bgrounding\b", r"\baground\b", r"\bstranded\b", r"\bran\s+aground\b", r"\brisk\s+of\s+grounding\b"]},
        "EXPLOSION": {"severity": "CRITICAL", "patterns": [r"\bexplosion\b", r"\bexploded\b", r"\bblast\b"]},
        "ATTACK": {"severity": "CRITICAL", "patterns": [r"\battack\b", r"\battacked\b", r"\bfired\s+upon\b", r"\bunder\s+fire\b", r"\bincoming\s+fire\b", r"\bmissile\s+attack\b"]},
        "AIR_ATTACK": {"severity": "CRITICAL", "patterns": [r"\bair\s+attack\b", r"\bairstrike\b", r"\bhostile\s+aircraft\b", r"\bfighter\s+jet\b", r"\bhelicopter\s+attack\b"]},
        "BOMB": {"severity": "CRITICAL", "patterns": [r"\bbomb\b", r"\bexplosive\s+device\b", r"\bIED\b", r"\bbomb\s+threat\b"]},
        "NAVAL_MINE": {"severity": "CRITICAL", "patterns": [r"\bsea\s+mine\b", r"\bfloating\s+mine\b", r"\bnaval\s+mine\b", r"\bminefield\b"]},
        "SUBMARINE": {"severity": "CRITICAL", "patterns": [r"\bsubmarine\b", r"\battack\s+submarine\b", r"\bmilitary\s+submarine\b"]},
        "PIRATES": {"severity": "CRITICAL", "patterns": [r"\bpirates?\b", r"\bpiracy\b", r"\barmed\s+boarding\b"]},
        "MILITARY": {"severity": "HIGH", "patterns": [r"\bmilitary\b", r"\bwarship\b", r"\bcoast\s+guard\b", r"\barmed\s+vessel\b"]},
        "HOSTAGE": {"severity": "CRITICAL", "patterns": [r"\bhostage\b", r"\bhijack\b", r"\bkidnapping\b", r"\babduction\b"]},
        "SABOTAGE": {"severity": "CRITICAL", "patterns": [r"\bsabotage\b", r"\bdeliberate\s+damage\b", r"\bmalicious\b"]},
        "UNAUTHORIZED_ACCESS": {"severity": "HIGH", "patterns": [r"\bintruder\b", r"\bunauthorized\b", r"\btrespassing\b"]},
        "UNAUTHORIZED_INTERCEPTION": {"severity": "HIGH", "patterns": [r"\battempt\s+to\s+stop\b", r"\bintercepted\s+by\s+unknown\b", r"\bblocked\s+by\s+unknown\b"]},
        "CIVIL_UNREST": {"severity": "MEDIUM", "patterns": [r"\briot\b", r"\bprotest\b", r"\bunrest\b"]},
        "TERRORISM": {"severity": "CRITICAL", "patterns": [r"\bterrorist\b", r"\bterrorism\b", r"\bsuicide\s+attack\b"]},
        "MEDICAL": {"severity": "HIGH", "patterns": [r"\bmedical\s+emergency\b", r"\bmedical\s+assistance\b", r"\binjured\b", r"\bwounded\b"]},
        "CASUALTY": {"severity": "CRITICAL", "patterns": [r"\bcasualty\b", r"\bmedical\s+evacuation\b", r"\bmedevac\b", r"\bcardiac\s+arrest\b", r"\bsevere\s+injury\b"]},
        "FATALITY": {"severity": "CRITICAL", "patterns": [r"\bfatality\b", r"\bdeath\b", r"\bdeceased\b"]},
        "RESCUE": {"severity": "HIGH", "patterns": [r"\brescue\b", r"\bSAR\b", r"\bsearch\s+and\s+rescue\b"]},
        "DISABLED": {"severity": "CRITICAL", "patterns": [r"\bdisabled\b", r"\blowerless\b", r"\bno\s+propulsion\b", r"\blost\s+power\b", r"\bblackout\b", r"\bengine\s+failure\b"]},
        "MACHINERY_FAILURE": {"severity": "HIGH", "patterns": [r"\bmachinery\s+failure\b", r"\bthruster\s+failure\b", r"\bgenerator\s+failure\b", r"\bcompressor\s+failure\b", r"\bloss\s+of\s+steering\b"]},
        "DRIFTING_OBJECT": {"severity": "HIGH", "patterns": [r"\bdrifting\s+object\b", r"\bfloating\s+object\b", r"\bderelict\b"]},
        "LISTING": {"severity": "HIGH", "patterns": [r"\blisting\b", r"\bheeling\b", r"\bunstable\b"]},
        "HURRICANE": {"severity": "CRITICAL", "patterns": [r"\bhurricane\b", r"\bcyclone\b", r"\btyphoon\b", r"\btropical\s+storm\b"]},
        "TSUNAMI": {"severity": "CRITICAL", "patterns": [r"\btsunami\b", r"\bseismic\s+sea\s+wave\b"]},
        "EXTREME_WAVES": {"severity": "HIGH", "patterns": [r"\bextreme\s+waves\b", r"\brogue\s+waves\b", r"\bheavy\s+seas\b", r"\bhigh\s+waves\b"]},
        "EXTREME_WIND": {"severity": "HIGH", "patterns": [r"\bstrong\s+wind\b", r"\bextreme\s+wind\b", r"\bgale\s+force\b", r"\bstorm\s+force\b"]},
        "COMMUNICATION": {"severity": "HIGH", "patterns": [r"\bcommunication\s+lost\b", r"\bVHF\s+failure\b", r"\bradio\s+failure\b"]},
        "NAVIGATION": {"severity": "HIGH", "patterns": [r"\bnavigation\s+failure\b", r"\bGPS\s+failure\b"]},
        "NEUTRAL_WATERS": {"severity": "HIGH", "patterns": [r"\bneutral\s+waters\b", r"\binternational\s+waters\b", r"\bterritorial\s+waters\b", r"\bEEZ\b"]},
        "ICE": {"severity": "HIGH", "patterns": [r"\biceberg\b", r"\bsea\s+ice\b", r"\bpack\s+ice\b", r"\bice\s+conditions\b"]},
        "VOLCANIC": {"severity": "HIGH", "patterns": [r"\bvolcanic\s+eruption\b", r"\bash\s+cloud\b"]},
        "EARTHQUAKE": {"severity": "HIGH", "patterns": [r"\bearthquake\b", r"\bseismic\s+activity\b"]},
        "OBJECT_TANKER": {"severity": "LOW", "patterns": [r"\btanker\b", r"\boil\s+tanker\b", r"\bLNG\s+tanker\b"]},
        "OBJECT_FSO": {"severity": "LOW", "patterns": [r"\bFSO\b", r"\bfloating\s+storage\s+offloading\b"]},
        "OBJECT_FPSO": {"severity": "LOW", "patterns": [r"\bFPSO\b", r"\bfloating\s+production\s+storage\s+offloading\b"]},
        "OBJECT_MOPU": {"severity": "LOW", "patterns": [r"\bMOPU\b", r"\bmobile\s+offshore\s+production\s+unit\b"]},
        "OBJECT_PLATFORM": {"severity": "LOW", "patterns": [r"\boffshore\s+platform\b", r"\bdrilling\s+platform\b"]},
        "OBJECT_NPP": {"severity": "LOW", "patterns": [r"\bnuclear\s+power\s+plant\b", r"\bNPP\b", r"\bnuclear\s+reactor\b"]},
        "OBJECT_REFINERY": {"severity": "LOW", "patterns": [r"\brefinery\b", r"\bpetrochemical\s+plant\b"]},
        "OBJECT_PORT": {"severity": "LOW", "patterns": [r"\bport\b", r"\bterminal\b", r"\boil\s+terminal\b"]},
    }

    NEGATION_PATTERNS = [r"\bno\b", r"\bnot\b", r"\bwithout\b", r"\bnever\b", r"\bruled\s+out\b", r"\bexcluded\b", r"\babsent\b", r"\bno\s+evidence\s+of\b", r"\bnot\s+detected\b"]
    UNCERTAINTY_PATTERNS = [r"\bsuspected\b", r"\bpossible\b", r"\bpossibly\b", r"\bprobable\b", r"\bprobably\b", r"\bmaybe\b", r"\bpotential\b", r"\bappears?\b", r"\bseems?\b", r"\bindicates?\b", r"\bsuggests?\b"]
    HISTORICAL_PATTERNS = [r"\bprevious\b", r"\bprior\b", r"\bhistorical\b", r"\bearlier\b", r"\blast\s+shift\b", r"\byesterday\b"]
    REPORTED_PATTERNS = [r"\breported\b", r"\bstated\b", r"\baccording\s+to\b"]
    CONFIRMED_PATTERNS = [r"\bconfirmed\b", r"\bverified\b", r"\bvalidated\b"]

    def normalize(self, text: str) -> dict:
        text = (text or "").strip()
        if not text:
            return self._empty_result()
        conditions = self._extract(text)
        active = [c for c in conditions if c["semantic_state"] in ("ACTIVE", "UNCERTAIN", "REPORTED", "CONFIRMED")]
        return {
            "critical_conditions": conditions,
            "critical_conditions_count": len(conditions),
            "event_type": self._determine_event_type(active),
            "severity": self._determine_overall_severity(active),
            "has_critical": any(c["severity"] == "CRITICAL" and c["semantic_state"] != "NEGATIVE" for c in active),
            "has_high": any(c["severity"] == "HIGH" and c["semantic_state"] != "NEGATIVE" for c in active),
            "semantic_summary": self._summary(conditions),
            "status": "NORMALIZED",
        }

    @staticmethod
    def _empty_result():
        return {
            "critical_conditions": [], "critical_conditions_count": 0,
            "event_type": "GENERAL", "severity": "LOW",
            "has_critical": False, "has_high": False,
            "semantic_summary": {
                "total_conditions": 0, "active_conditions": 0, "uncertain_conditions": 0,
                "negative_conditions": 0, "historical_conditions": 0,
                "reported_conditions": 0, "confirmed_conditions": 0,
                "average_confidence": 0.0,
            },
            "status": "NORMALIZED",
        }

    def _extract(self, text: str) -> list:
        found = []
        sentence_spans = list(re.finditer(r"[^.!?]+(?:[.!?]+|$)", text, flags=re.DOTALL))
        for condition_type, config in self.CONDITIONS.items():
            best = None
            for pattern in config["patterns"]:
                match = re.search(pattern, text, flags=re.IGNORECASE)
                if not match:
                    continue
                sentence = self._sentence_for_position(text, match.start(), sentence_spans)
                sentence_start = sentence["start"]
                sentence_text = sentence["text"]
                local_position = match.start() - sentence_start
                local_end = match.end() - sentence_start
                before = sentence_text[:local_position]
                after = sentence_text[local_end:]
                semantic_state = self._classify_local(before, after)
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
                    "uncertainty": "HIGH" if semantic_state == "UNCERTAIN" else None,
                    "negation_found": semantic_state == "NEGATIVE",
                    "uncertainty_found": semantic_state == "UNCERTAIN",
                    "temporal_context": self._temporal_context_local(before, after),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "source": "INCIDENT_INPUT",
                    "status": "ACTIVE" if semantic_state not in ("NEGATIVE", "HISTORICAL") else "EXCLUDED",
                }
                if best is None or self._state_rank(semantic_state) > self._state_rank(best["semantic_state"]):
                    best = candidate
            if best:
                found.append(best)
        return found

    @staticmethod
    def _sentence_for_position(text, position, spans):
        for span in spans:
            if span.start() <= position < span.end():
                return {"start": span.start(), "end": span.end(), "text": span.group(0)}
        return {"start": 0, "end": len(text), "text": text}

    @staticmethod
    def _local_modifier_before(before, patterns, max_words=7):
        words = re.findall(r"\b[\w'-]+\b", before.lower())
        return any(re.search(p, " ".join(words[-max_words:]), flags=re.IGNORECASE) for p in patterns)

    @staticmethod
    def _local_modifier_after(after, patterns, max_words=7):
        words = re.findall(r"\b[\w'-]+\b", after.lower())
        return any(re.search(p, " ".join(words[:max_words]), flags=re.IGNORECASE) for p in patterns)

    def _classify_local(self, before, after):
        if self._local_modifier_before(before, self.HISTORICAL_PATTERNS):
            return "HISTORICAL"
        if self._local_modifier_before(before, self.NEGATION_PATTERNS):
            return "NEGATIVE"
        if self._local_modifier_before(before, self.UNCERTAINTY_PATTERNS) or self._local_modifier_after(after, self.UNCERTAINTY_PATTERNS):
            return "UNCERTAIN"
        if self._local_modifier_before(before, self.CONFIRMED_PATTERNS) or self._local_modifier_after(after, self.CONFIRMED_PATTERNS):
            return "CONFIRMED"
        if self._local_modifier_before(before, self.REPORTED_PATTERNS) or self._local_modifier_after(after, self.REPORTED_PATTERNS):
            return "REPORTED"
        return "ACTIVE"

    @staticmethod
    def _temporal_context_local(before, after):
        if SemanticEventNormalizer._local_modifier_before(before, SemanticEventNormalizer.HISTORICAL_PATTERNS):
            return "PREVIOUS"
        if SemanticEventNormalizer._local_modifier_before(before, SemanticEventNormalizer.CONFIRMED_PATTERNS) or SemanticEventNormalizer._local_modifier_after(after, SemanticEventNormalizer.CONFIRMED_PATTERNS):
            return "CONFIRMED"
        if SemanticEventNormalizer._local_modifier_before(before, SemanticEventNormalizer.REPORTED_PATTERNS) or SemanticEventNormalizer._local_modifier_after(after, SemanticEventNormalizer.REPORTED_PATTERNS):
            return "REPORTED"
        return "CURRENT"

    @staticmethod
    def _state_rank(state):
        return {"NEGATIVE": 0, "HISTORICAL": 1, "REPORTED": 2, "UNCERTAIN": 3, "ACTIVE": 4, "CONFIRMED": 5}.get(state, 0)

    @staticmethod
    def _polarity(state):
        if state == "NEGATIVE": return "NEGATIVE"
        if state == "UNCERTAIN": return "NEUTRAL"
        return "POSITIVE"

    @staticmethod
    def _confidence(state):
        return {"NEGATIVE": 0.95, "HISTORICAL": 0.90, "REPORTED": 0.70, "UNCERTAIN": 0.60, "ACTIVE": 0.80, "CONFIRMED": 0.95}.get(state, 0.50)

    @staticmethod
    def _determine_event_type(conditions):
        if not conditions:
            return "GENERAL"
        critical = [c for c in conditions if c["severity"] == "CRITICAL"]
        if critical:
            critical.sort(key=lambda c: (SemanticEventNormalizer._state_rank(c["semantic_state"]), c["confidence"]), reverse=True)
            return critical[0]["condition"]
        high = [c for c in conditions if c["severity"] == "HIGH"]
        if high:
            high.sort(key=lambda c: c["confidence"], reverse=True)
            return high[0]["condition"]
        return conditions[0]["condition"]

    @staticmethod
    def _determine_overall_severity(conditions):
        if any(c["severity"] == "CRITICAL" for c in conditions):
            return "CRITICAL"
        if any(c["severity"] == "HIGH" for c in conditions):
            return "HIGH"
        return "LOW"

    @staticmethod
    def _summary(conditions):
        if not conditions:
            return {"total_conditions": 0, "active_conditions": 0, "uncertain_conditions": 0, "negative_conditions": 0, "historical_conditions": 0, "reported_conditions": 0, "confirmed_conditions": 0, "average_confidence": 0.0}
        states = [c["semantic_state"] for c in conditions]
        return {
            "total_conditions": len(conditions),
            "active_conditions": states.count("ACTIVE"),
            "uncertain_conditions": states.count("UNCERTAIN"),
            "negative_conditions": states.count("NEGATIVE"),
            "historical_conditions": states.count("HISTORICAL"),
            "reported_conditions": states.count("REPORTED"),
            "confirmed_conditions": states.count("CONFIRMED"),
            "average_confidence": round(sum(c["confidence"] for c in conditions) / len(conditions), 3),
        }


# ===========================================================================
# STREAMLIT UI — v0.5.2 Constitution-Aligned Sequential
# ===========================================================================

st.set_page_config(page_title="AVCS Virtual Company", page_icon="🧭", layout="wide")

# --- WELCOME SCREEN ---
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
            unsafe_allow_html=True,
        )
        if st.button("▸ ENTER COMMAND CENTER", use_container_width=True, type="primary"):
            st.session_state.welcome_shown = True
            st.rerun()
    st.stop()

st.title("🧭 AVCS VIRTUAL COMPANY")
st.caption("AI-Driven Operational Decision Architecture — v0.5.2 Constitution-Aligned Sequential")

# --- SESSION INIT ---
defaults = {
    "initialized": True,
    "event_id": None,
    "current_step": "input",
    "event_data": None,
    "department_results": None,
    "aggregated_state": None,
    "conflict_result": None,
    "decision_proposal": None,
    "authority_state": None,
    "authorized": None,
    "incident_text": "",
    "object_type": "",
    "position": "",
    "heading": 0,
    "speed": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

normalizer = SemanticEventNormalizer()

# --- SIDEBAR ---
with st.sidebar:
    try:
        st.image("app/logo.png", width=200)
    except:
        st.markdown("### 🧭 AVCS")

    st.divider()
    st.header("System Status")
    st.info(f"Event: {st.session_state.event_id}" if st.session_state.get("event_id") else "No active event")
    st.write(f"Step: {st.session_state.current_step}")
    st.divider()
    st.header("Architecture")
    st.caption("INCIDENT → SEMANTIC → SEQUENTIAL EXECUTOR → 7 Dpts. (INS-A) → AGGREGATION → CONFLICT → DECISION → AUTHORITY → RECORD")
    st.divider()
    st.caption("Version: 0.5.2")

    if st.button("🔄 Reset Event", use_container_width=True):
        for key in ["event_id", "event_data", "department_results",
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

# --- TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📥 Incident Input",
    "⚙️ Processing",
    "📋 Decision",
    "📊 Record",
    "📋 Incident Registry",
])

# ===========================================================================
# TAB 1: INCIDENT INPUT
# ===========================================================================

with tab1:
    st.header("Incident Input")
    st.caption("Describe any incident — the system will classify and process it automatically.")

    incident_description = st.text_area(
        "Incident Description",
        value=st.session_state.incident_text,
        height=150,
        placeholder="Describe the incident in detail...",
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
                "object": object_type or "Unknown",
                "position": position or "Unknown",
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

# ===========================================================================
# TAB 2: PROCESSING — SEQUENTIAL EXECUTION (v0.5.2)
# ===========================================================================

with tab2:
    st.header("Processing Pipeline")
    st.caption("Sequential execution — Constitution-aligned (v0.5.2)")

    if st.session_state.current_step == "processing" and st.session_state.event_data:
        with st.spinner("Processing incident (sequential)..."):
            # ---------------------------------------------------------------
            # Initialize departments IN ORDER
            # ---------------------------------------------------------------
            departments = [
                LookoutDepartment(),
                ChartsDepartment(),
                GyroDepartment(),
                NavigatorDepartment(),
                CompassDepartment(),
                HelmDepartment(),
                CaptainDepartment(),
            ]

            # ---------------------------------------------------------------
            # Initialize components
            # ---------------------------------------------------------------
            state_machine = StateMachine()
            aggregator = Aggregator()
            conflict_detector = ConflictDetector()
            decision_engine = DecisionEngine()
            authority_gate = AuthorityGate()

            # ---------------------------------------------------------------
            # Initialize SequentialExecutor
            # ---------------------------------------------------------------
            executor = SequentialExecutor(
                departments=departments,
                state_machine=state_machine,
                aggregator=aggregator,
                conflict_detector=conflict_detector,
                decision_engine=decision_engine,
                authority_gate=authority_gate,
            )

            # ---------------------------------------------------------------
            # Prepare event data
            # ---------------------------------------------------------------
            event_data = st.session_state.event_data.copy()

            event_data["observations"] = event_data.get("critical_conditions", [])
            event_data["facts"] = [
                f"Object: {event_data.get('object')}",
                f"Position: {event_data.get('position')}",
            ]
            event_data["operational_state"] = {
                "structural_integrity": True,
                "human_safety": True,
                "operational_control": True,
            }
            event_data["human_condition"] = "READY"
            event_data["system_condition"] = "NOMINAL"
            event_data["load_level"] = "MEDIUM"
            event_data["current_state"] = {
                "event_type": event_data.get("event_type"),
                "severity": event_data.get("severity"),
            }

            # ---------------------------------------------------------------
            # Execute sequentially
            # ---------------------------------------------------------------
            result = executor.execute(event_data)

            # ---------------------------------------------------------------
            # Store results
            # ---------------------------------------------------------------
            st.session_state.department_results = result["department_results"]
            st.session_state.aggregated_state = result["aggregated_state"]
            st.session_state.conflict_result = result["conflict_result"]
            st.session_state.decision_proposal = result["decision_proposal"]
            st.session_state.authority_state = result["authority_state"]
            st.session_state.event_id = result["event_id"]
            st.session_state.current_step = "authority"

            # ---------------------------------------------------------------
            # Update registry
            # ---------------------------------------------------------------
            registry = IncidentRegistry()
            registry.update_incident(
                st.session_state.event_id,
                {
                    "decision_proposal": result["decision_proposal"],
                    "authorized": False,
                    "status": "AWAITING_AUTHORITY",
                },
            )

            st.rerun()

    # ---------------------------------------------------------------
    # Display: Department Results (INS-A)
    # ---------------------------------------------------------------
    if st.session_state.get("department_results"):
        st.subheader("Department Assessments (INS-A — Sequential)")
        for dept, result in st.session_state.department_results.items():
            with st.expander(f"📋 {dept}"):
                if isinstance(result, dict) and "error" in result:
                    st.error(result["error"])
                elif isinstance(result, dict) and result.get("status") == "FAILED":
                    st.error(result.get("assessment", "FAILED"))
                    st.json(result)
                else:
                    st.json(result)

    # ---------------------------------------------------------------
    # Display: Aggregated State + Structural Fields
    # ---------------------------------------------------------------
    if st.session_state.get("aggregated_state"):
        st.subheader("📊 Aggregated State")

        structural = st.session_state.aggregated_state.get("structural", {})
        if structural:
            st.markdown("### 🧭 Structural Fields (INS-A)")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("North", structural.get("north_status", "—"))
                st.metric("Veto", "YES" if structural.get("veto") else "NO")
            with col2:
                st.metric("Stability", structural.get("stability_status", "—"))
                st.metric("Load", structural.get("load_level", "—"))
            with col3:
                st.metric("Reality", structural.get("reality_status", "—"))
                st.metric("Coherence", structural.get("structural_coherence", "—"))

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Signal", structural.get("signal_state", "—"))
            with col2:
                st.metric("Course", structural.get("course_state", "—"))
            with col3:
                st.metric("Decision", structural.get("decision_state", "—"))

            with st.expander("Full Structural State"):
                st.json(structural)

        with st.expander("Full Aggregated State"):
            st.json(st.session_state.aggregated_state)

    # ---------------------------------------------------------------
    # Display: Conflict Detection
    # ---------------------------------------------------------------
    if st.session_state.get("conflict_result"):
        st.subheader("⚠️ Conflict Detection")
        cr = st.session_state.conflict_result

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Has Conflicts", "YES" if cr.get("has_conflicts") else "NO")
        with col2:
            st.metric("Conflict Type", cr.get("conflict_type", "NONE"))
        with col3:
            st.metric("Decision Blocked", "YES" if cr.get("decision_blocked") else "NO")

        if cr.get("has_conflicts"):
            st.warning(f"{len(cr.get('conflicts', []))} conflict(s) detected")
            for c in cr.get("conflicts", []):
                st.markdown(
                    f"- **{c.get('type')}** ({c.get('severity')}): "
                    f"{c.get('description')}"
                )
        else:
            st.success("No structural conflicts detected")

        with st.expander("Full Conflict Result"):
            st.json(cr)

# ===========================================================================
# TAB 3: DECISION
# ===========================================================================

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
                        "status": "AUTHORIZED",
                    })
                    st.rerun()
            with col2:
                if st.button("❌ Reject", type="secondary"):
                    st.session_state.authorized = False
                    st.session_state.current_step = "completed"
                    registry = IncidentRegistry()
                    registry.update_incident(st.session_state.event_id, {
                        "authorized": False,
                        "status": "REJECTED",
                    })
                    st.rerun()

        if st.session_state.get("authorized") is True:
            st.success("✅ Decision Authorized")
            st.session_state.current_step = "completed"
        elif st.session_state.get("authorized") is False:
            st.error("❌ Decision Rejected")

# ===========================================================================
# TAB 4: RECORD
# ===========================================================================

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
            "conflict_result": st.session_state.conflict_result,
        }

        st.json(record)

        st.download_button(
            label="📥 Download AVCS Record",
            data=json.dumps(record, indent=2),
            file_name=f"AVCS_RECORD_{st.session_state.event_id}.json",
            mime="application/json",
        )
    else:
        st.info("Complete the decision cycle to generate AVCS Record")

# ===========================================================================
# TAB 5: INCIDENT REGISTRY
# ===========================================================================

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
                            st.write(
                                f"- {cond.get('condition', 'UNKNOWN')} "
                                f"({cond.get('severity', 'UNKNOWN')}) — "
                                f"{cond.get('semantic_state', 'UNKNOWN')} "
                                f"/ confidence {cond.get('confidence', 0):.2f}"
                            )

                if st.button("View Record", key=f"view_{incident['event_id']}"):
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

    with col2:
        if st.button("🗑️ Clear All Records (Danger)"):
            confirm = st.checkbox("I understand this will delete ALL records", key="confirm_clear_all")
            if confirm:
                count = registry.clear_all()
                st.warning(f"Deleted {count} records.")
                st.rerun()
