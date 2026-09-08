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
        # ========== УГРОЗЫ И ИНЦИДЕНТЫ ==========
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
        "COLLISION_RISK": {"severity": "CRITICAL", "patterns": [r"\bcollision\s+risk\b", r"\bcollision\s+hazard\b", r"\brisk\s+of\s+collision\b", r"\bdanger\s+of\s+collision\b", r"\bpotential\s+collision\b", r"\bimminent\s+collision\b", r"\bclose\s+quarters\s+situation\b", r"\bCPA\s+less\s+than\b", r"\bTCPA\s+less\s+than\b", r"\bon\s+collision\s+course\b", r"\bconverging\s+course\b", r"\brisk\s+of\s+impact\b", r"\bpossible\s+collision\b", r"\bapproaching\s+vessel\b", r"\bclosing\s+speed\b", r"\bhigh\s+risk\s+of\s+collision\b"]},
        "GROUNDING": {"severity": "CRITICAL", "patterns": [r"\bgrounding\b", r"\baground\b", r"\bstranded\b", r"\bran\s+aground\b", r"\brisk\s+of\s+grounding\b", r"\bthreat\s+of\s+grounding\b"]},
        "EXPLOSION": {"severity": "CRITICAL", "patterns": [r"\bexplosion\b", r"\bexploded\b", r"\bblast\b"]},
        "ATTACK": {"severity": "CRITICAL", "patterns": [r"\battack\b", r"\battacked\b", r"\bfired\s+upon\b", r"\bfired\s+at\b", r"\bshelling\b", r"\bshelled\b", r"\bhit\s+by\s+shell\b", r"\bstruck\s+by\s+round\b", r"\bmortar\s+attack\b", r"\bmissile\s+attack\b", r"\bair\s+strike\b", r"\bgunned\s+down\b", r"\bsprayed\s+with\s+bullets\b", r"\bunder\s+fire\b", r"\bincoming\s+fire\b", r"\bexplosion\s+nearby\b", r"\bblast\s+distance\b"]},
        "AIR_ATTACK": {"severity": "CRITICAL", "patterns": [r"\bair\s+attack\b", r"\baerial\s+attack\b", r"\baircraft\s+threat\b", r"\bhostile\s+aircraft\b", r"\bmilitary\s+aircraft\b", r"\bfighter\s+jet\b", r"\bairstrike\b", r"\bair\s+strike\b", r"\bfixed\s+wing\s+aircraft\b", r"\bhelicopter\s+attack\b", r"\battack\s+helicopter\b"]},
        "BOMB": {"severity": "CRITICAL", "patterns": [r"\bbomb\b", r"\bexplosive\b", r"\bexplosive\s+device\b", r"\bIED\b", r"\bimprovised\s+explosive\b", r"\bbomb\s+threat\b"]},
        "NAVAL_MINE": {"severity": "CRITICAL", "patterns": [r"\bmine\b", r"\bsea\s+mine\b", r"\bfloating\s+mine\b", r"\bnaval\s+mine\b", r"\bminefield\b", r"\bmine\s+threat\b"]},
        "SUBMARINE": {"severity": "CRITICAL", "patterns": [r"\bsubmarine\b", r"\battack\s+submarine\b", r"\bnaval\s+submarine\b", r"\bsub\b", r"\bunderwater\s+vessel\b", r"\bmilitary\s+submarine\b"]},
        "PIRATES": {"severity": "CRITICAL", "patterns": [r"\bpirates?\b", r"\bpirate\b", r"\bpiracy\b", r"\barmed\s+boarding\b", r"\bsecurity\s+threat\b"]},
        "MILITARY": {"severity": "HIGH", "patterns": [r"\bmilitary\b", r"\bnaval\b", r"\bwarship\b", r"\bcoast\s+guard\b", r"\barmed\s+vessel\b"]},
        "HOSTAGE": {"severity": "CRITICAL", "patterns": [r"\bhostage\b", r"\bhijack\b", r"\bkidnapping\b", r"\babduction\b", r"\bseizure\b"]},
        "SABOTAGE": {"severity": "CRITICAL", "patterns": [r"\bsabotage\b", r"\bdeliberate\s+damage\b", r"\bintentional\b", r"\bmalicious\b"]},
        "UNAUTHORIZED_ACCESS": {"severity": "HIGH", "patterns": [r"\bintruder\b", r"\bunauthorized\b", r"\btrespassing\b", r"\bbreach\s+of\s+security\b"]},
        "UNAUTHORIZED_INTERCEPTION": {"severity": "HIGH", "patterns": [r"\bunauthorized\s+interception\b", r"\battempt\s+to\s+stop\b", r"\btrying\s+to\s+stop\b", r"\bintercepted\s+by\s+unknown\b", r"\bapproached\s+by\s+unidentified\b", r"\bblocked\s+by\s+unknown\b", r"\bforced\s+to\s+stop\b"]},
        "CIVIL_UNREST": {"severity": "MEDIUM", "patterns": [r"\briot\b", r"\bprotest\b", r"\bunrest\b", r"\bdemonstration\b"]},
        "TERRORISM": {"severity": "CRITICAL", "patterns": [r"\bterrorist\b", r"\bterrorism\b", r"\bbomb\s+threat\b", r"\bsuicide\s+attack\b"]},
        "MEDICAL": {"severity": "HIGH", "patterns": [r"\bmedical\s+emergency\b", r"\bmedical\s+assistance\b", r"\binjured\b", r"\bwounded\b", r"\bmedical\s+help\b", r"\bserious\s+injury\b", r"\blife\s+threatening\b"]},
        "CASUALTY": {"severity": "CRITICAL", "patterns": [r"\binjured\s+person\b", r"\bperson\s+injured\b", r"\bcasualty\b", r"\bcasualties\b", r"\bmedical\s+evacuation\b", r"\bmedevac\b", r"\btrauma\b", r"\bfracture\b", r"\bburn\s+injury\b", r"\bthermal\s+injury\b", r"\bchemical\s+burn\b", r"\bcardiac\s+arrest\b", r"\bheart\s+attack\b", r"\bunconscious\b", r"\bcollapsed\b", r"\bpoisoning\b", r"\btoxic\s+exposure\b", r"\bchemical\s+exposure\b", r"\bhemorrhage\b", r"\bblood\s+loss\b", r"\bwound\b", r"\blaceration\b", r"\bamputation\b", r"\bcrush\s+injury\b", r"\bspinal\s+injury\b", r"\bhead\s+trauma\b", r"\bbrain\s+injury\b", r"\bsevere\s+injury\b", r"\blife-threatening\s+injury\b"]},
        "FATALITY": {"severity": "CRITICAL", "patterns": [r"\bfatality\b", r"\bdeath\b", r"\bcasualty\b", r"\bdeceased\b"]},
        "RESCUE": {"severity": "HIGH", "patterns": [r"\brescue\b", r"\brescue\s+operation\b", r"\bSAR\b", r"\bsearch\s+and\s+rescue\b"]},
        "DISABLED": {"severity": "CRITICAL", "patterns": [r"\bdisabled\b", r"\blowerless\b", r"\bdead\s+in\s+the\s+water\b", r"\bno\s+propulsion\b", r"\blost\s+power\b", r"\bpower\s+loss\b", r"\bengine\s+failure\b", r"\bmachinery\s+breakdown\b", r"\bmechanical\s+failure\b", r"\bunable\s+to\s+manoeuvre\b", r"\bloss\s+of\s+steering\b", r"\brudder\s+failure\b", r"\bblackout\b", r"\btotal\s+power\s+loss\b", r"\bcomplete\s+power\s+failure\b", r"\bpropulsion\s+lost\b", r"\bthruster\s+failure\b", r"\bdynamic\s+positioning\s+lost\b"]},
        "MACHINERY_FAILURE": {"severity": "HIGH", "patterns": [r"\bmachinery\s+failure\b", r"\bmechanical\s+failure\b", r"\bequipment\s+failure\b", r"\bthruster\s+failure\b", r"\bthruster\s+outage\b", r"\bthruster\s+loss\b", r"\bbow\s+thruster\s+failure\b", r"\bstern\s+thruster\s+failure\b", r"\bazimuth\s+thruster\s+failure\b", r"\bengine\s+failure\b", r"\bmain\s+engine\s+failure\b", r"\bengine\s+breakdown\b", r"\bengine\s+trip\b", r"\bengine\s+shutdown\b", r"\bauxiliary\s+engine\s+failure\b", r"\bauxiliary\s+engine\s+trip\b", r"\bgenerator\s+failure\b", r"\bgenerator\s+trip\b", r"\bpower\s+generation\s+failure\b", r"\bcompressor\s+failure\b", r"\bair\s+compressor\s+failure\b", r"\bcompressor\s+trip\b", r"\bloss\s+of\s+compressed\s+air\b", r"\bsteering\s+gear\s+failure\b", r"\brudder\s+failure\b", r"\bloss\s+of\s+steering\b", r"\bunable\s+to\s+steer\b", r"\bpropulsion\s+failure\b", r"\bpropulsion\s+loss\b", r"\bblackout\b", r"\btotal\s+power\s+loss\b", r"\bcomplete\s+power\s+failure\b", r"\bpower\s+outage\b"]},
        "DRIFTING_OBJECT": {"severity": "HIGH", "patterns": [r"\bdrifting\s+object\b", r"\bfloating\s+object\b", r"\bunidentified\s+floating\b", r"\bderelict\b", r"\bfloating\s+hazard\b"]},
        "LISTING": {"severity": "HIGH", "patterns": [r"\blisting\b", r"\bheeling\b", r"\bunstable\b", r"\bleaning\b", r"\btilting\b"]},
        "HURRICANE": {"severity": "CRITICAL", "patterns": [r"\bhurricane\b", r"\bcyclone\b", r"\btyphoon\b", r"\btropical\s+storm\b"]},
        "TSUNAMI": {"severity": "CRITICAL", "patterns": [r"\btsunami\b", r"\bmega\s+tsunami\b", r"\bseismic\s+sea\s+wave\b"]},
        "EXTREME_WAVES": {"severity": "HIGH", "patterns": [r"\bextreme\s+waves\b", r"\brogue\s+waves\b", r"\bgiant\s+waves\b", r"\bheavy\s+seas\b", r"\bhigh\s+waves\b", r"\bwave\s+height\s+exceeds\b", r"\bmonster\s+waves\b"]},
        "EXTREME_WIND": {"severity": "HIGH", "patterns": [r"\bstrong\s+wind\b", r"\bhigh\s+wind\b", r"\bextreme\s+wind\b", r"\bgale\s+force\b", r"\bstorm\s+force\b", r"\bhurricane\s+force\b", r"\bwind\s+speed\s+exceeds\b", r"\bsevere\s+gale\b"]},
        "COMMUNICATION": {"severity": "HIGH", "patterns": [r"\bcommunication\s+lost\b", r"\bVHF\s+failure\b", r"\bno\s+contact\b", r"\bradio\s+failure\b"]},
        "NAVIGATION": {"severity": "HIGH", "patterns": [r"\bnavigation\s+failure\b", r"\bGPS\s+failure\b", r"\bunable\s+to\s+navigate\b"]},
        "NEUTRAL_WATERS": {"severity": "HIGH", "patterns": [r"\bneutral\s+waters\b", r"\binternational\s+waters\b", r"\bterritorial\s+waters\b", r"\bexclusive\s+economic\s+zone\b", r"\bEEZ\b", r"\bcoastal\s+waters\b", r"\bcontiguous\s+zone\b"]},
        "ICE": {"severity": "HIGH", "patterns": [r"\bice\b", r"\biceberg\b", r"\bsea\s+ice\b", r"\bpack\s+ice\b", r"\bice\s+conditions\b"]},
        "VOLCANIC": {"severity": "HIGH", "patterns": [r"\bvolcanic\s+eruption\b", r"\bash\s+cloud\b", r"\bvolcanic\s+activity\b"]},
        "EARTHQUAKE": {"severity": "HIGH", "patterns": [r"\bearthquake\b", r"\bseismic\s+activity\b", r"\btremors\b"]},

        # ========== ГРАЖДАНСКИЕ ОБЪЕКТЫ ==========
        "OBJECT_TANKER": {"severity": "LOW", "patterns": [r"\btanker\b", r"\boil\s+tanker\b", r"\bchemical\s+tanker\b", r"\bLNG\s+tanker\b", r"\bLPG\s+tanker\b"]},
        "OBJECT_FSO": {"severity": "LOW", "patterns": [r"\bFSO\b", r"\bfloating\s+storage\s+offloading\b"]},
        "OBJECT_FPSO": {"severity": "LOW", "patterns": [r"\bFPSO\b", r"\bfloating\s+production\s+storage\s+offloading\b"]},
        "OBJECT_MOPU": {"severity": "LOW", "patterns": [r"\bMOPU\b", r"\bmobile\s+offshore\s+production\s+unit\b"]},
        "OBJECT_PLATFORM": {"severity": "LOW", "patterns": [r"\bplatform\b", r"\boffshore\s+platform\b", r"\bdrilling\s+platform\b", r"\bproduction\s+platform\b"]},
        "OBJECT_NPP": {"severity": "LOW", "patterns": [r"\bnuclear\s+power\s+plant\b", r"\bNPP\b", r"\batom\s+station\b", r"\bnuclear\s+reactor\b"]},
        "OBJECT_REFINERY": {"severity": "LOW", "patterns": [r"\brefinery\b", r"\boil\s+refinery\b", r"\bpetrochemical\s+plant\b", r"\brefinery\s+plant\b"]},
        "OBJECT_PORT": {"severity": "LOW", "patterns": [r"\bport\b", r"\bterminal\b", r"\bsea\s+port\b", r"\boil\s+terminal\b", r"\bcontainer\s+terminal\b"]},
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
                "
