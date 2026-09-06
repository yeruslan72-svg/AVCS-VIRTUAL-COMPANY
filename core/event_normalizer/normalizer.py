```python
"""
AVCS VIRTUAL COMPANY
Event Normalizer

EXTRACT critical conditions from raw incident description
PRESERVE all critical information
PASS structured conditions to Dispatcher

Architecture:
    RAW INCIDENT
          ↓
    EVENT NORMALIZER
          ↓
    SEMANTIC ANALYZER
          ↓
    SEMANTIC STATE
          ↓
    CRITICAL CONDITIONS
          ↓
    DISPATCHER

Version: v0.3.7 — Semantic Analyzer Integration
"""

from typing import Dict, Any, List
from datetime import datetime, timezone

from core.semantic_analyzer import SemanticAnalyzer


class EventNormalizer:
    """
    Event Normalizer extracts critical conditions from incident descriptions.

    IMPORTANT ARCHITECTURAL RULE:

    EventNormalizer does NOT independently interpret semantic meaning.

    Semantic meaning is determined by SemanticAnalyzer.

    EventNormalizer:
        1. identifies candidate critical conditions
        2. sends them to SemanticAnalyzer
        3. preserves the semantic result
        4. excludes only explicitly negative / historical conditions
        5. preserves uncertain conditions
        6. passes structured conditions to Dispatcher

    Semantic states:

        POSITIVE
            Condition is asserted as present.

        NEGATIVE
            Condition is explicitly denied / ruled out.

        NEUTRAL + HIGH uncertainty
            Condition is possible / suspected / uncertain.

        PREVIOUS
            Condition belongs to a previous / historical state.

    Critical principle:

        UNCERTAIN != ABSENT

    An uncertain critical condition must NOT be silently discarded.
    """

    # ------------------------------------------------------------------
    # CRITICAL CONDITION DICTIONARY
    # ------------------------------------------------------------------

    CRITICAL_KEYWORDS = {
        "fire": {
            "severity": "CRITICAL",
            "keywords": [
                "fire",
                "flame",
                "burning",
                "ignition",
            ],
        },

        "smoke": {
            "severity": "HIGH",
            "keywords": [
                "smoke",
                "fume",
            ],
        },

        "evacuation": {
            "severity": "CRITICAL",
            "keywords": [
                "evacuate",
                "evacuating",
                "abandon",
            ],
        },

        "temperature": {
            "severity": "HIGH",
            "keywords": [
                "temperature",
                "heat",
                "overheat",
            ],
        },

        "oil_spill": {
            "severity": "CRITICAL",
            "keywords": [
                "oil spill",
                "spill",
                "leak",
                "pollution",
                "environmental",
            ],
        },

        "hull_breach": {
            "severity": "CRITICAL",
            "keywords": [
                "water ingress",
                "breach",
                "hull",
                "flood",
            ],
        },

        "man_overboard": {
            "severity": "CRITICAL",
            "keywords": [
                "man overboard",
                "overboard",
                "MOB",
            ],
        },

        "gas_leak": {
            "severity": "CRITICAL",
            "keywords": [
                "gas leak",
                "methane",
                "toxic",
            ],
        },

        "drone": {
            "severity": "HIGH",
            "keywords": [
                "drone",
                "UAV",
                "unidentified",
            ],
        },

        "collision": {
            "severity": "CRITICAL",
            "keywords": [
                "collision",
                "impact",
                "strike",
            ],
        },

        "explosion": {
            "severity": "CRITICAL",
            "keywords": [
                "explosion",
                "blast",
                "boom",
            ],
        },
    }

    # ------------------------------------------------------------------
    # INITIALIZATION
    # ------------------------------------------------------------------

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

        self.critical_conditions: List[Dict[str, Any]] = []

        self.semantic_analyzer = SemanticAnalyzer()

        self.last_debug: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # MAIN NORMALIZATION
    # ------------------------------------------------------------------

    def normalize(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize raw incident data.

        Input:
            {
                "description": "...",
                "object": "...",
                "position": "...",
                ...
            }

        Output:
            normalized event with structured semantic conditions.
        """

        description = input_data.get("description", "")

        object_type = input_data.get(
            "object",
            "Unknown"
        )

        position = input_data.get(
            "position",
            "Unknown"
        )

        # --------------------------------------------------------------
        # EXTRACT CONDITIONS
        # --------------------------------------------------------------

        critical_conditions, debug_info = (
            self._extract_critical_conditions(description)
        )

        self.critical_conditions = critical_conditions
        self.last_debug = debug_info

        # --------------------------------------------------------------
        # EVENT TYPE
        # --------------------------------------------------------------

        event_type = self._determine_event_type(
            critical_conditions
        )

        # --------------------------------------------------------------
        # OVERALL SEVERITY
        # --------------------------------------------------------------

        severity = self._determine_overall_severity(
            critical_conditions
        )

        is_emergency = severity in [
            "CRITICAL",
            "HIGH",
        ]

        # --------------------------------------------------------------
        # SEMANTIC SUMMARY
        # --------------------------------------------------------------

        semantic_summary = self._build_semantic_summary(
            critical_conditions
        )

        # --------------------------------------------------------------
        # TIMESTAMP
        # --------------------------------------------------------------

        timestamp = self._utc_timestamp()

        # --------------------------------------------------------------
        # EVENT ID
        # --------------------------------------------------------------

        event_id = input_data.get(
            "event_id",
            f"EVT-{datetime.now(timezone.utc).strftime('%Y%m%d')}-001"
        )

        # --------------------------------------------------------------
        # NORMALIZED DATA
        # --------------------------------------------------------------

        normalized_data = {
            "event_id": event_id,

            "raw_description": description,

            "object": object_type,

            "position": position,

            "timestamp": timestamp,

            "event_type": event_type,

            "severity": severity,

            "is_emergency": is_emergency,

            "critical_conditions": critical_conditions,

            "critical_conditions_count": len(
                critical_conditions
            ),

            "has_critical": any(
                c.get("severity") == "CRITICAL"
                for c in critical_conditions
            ),

            "has_high": any(
                c.get("severity") == "HIGH"
                for c in critical_conditions
            ),

            "semantic_summary": semantic_summary,

            "debug_info": debug_info,

            "status": "NORMALIZED",
        }

        # Preserve original input and add normalized data.
        return {
            **input_data,
            **normalized_data,
        }

    # ------------------------------------------------------------------
    # CRITICAL CONDITION EXTRACTION
    # ------------------------------------------------------------------

    def _extract_critical_conditions(
        self,
        text: str,
    ):
        """
        Extract critical conditions and apply SemanticAnalyzer.

        IMPORTANT:

            NEGATIVE  -> exclude
            PREVIOUS  -> exclude
            UNCERTAIN -> preserve
            POSITIVE  -> preserve
            CONFIRMED  -> preserve

        This method does NOT perform independent semantic interpretation.
        """

        conditions: List[Dict[str, Any]] = []

        debug_info: Dict[str, Any] = {
            "semantic_analyzer": "ACTIVE",
            "semantic_analyzer_version": "v0.3.x",
            "checks": [],
            "keyword_results": {},
        }

        if not text:
            return conditions, debug_info

        text_lower = text.lower()

        # --------------------------------------------------------------
        # LOOP THROUGH CRITICAL CONDITIONS
        # --------------------------------------------------------------

        for condition_type, config in self.CRITICAL_KEYWORDS.items():

            for keyword in config["keywords"]:

                keyword_lower = keyword.lower()

                if keyword_lower not in text_lower:
                    continue

                # ------------------------------------------------------
                # SEMANTIC ANALYSIS
                # ------------------------------------------------------

                analysis = self.semantic_analyzer.analyze(
                    text,
                    keyword,
                )

                # ------------------------------------------------------
                # DEBUG RECORD
                # ------------------------------------------------------

                check_result = {
                    "condition": condition_type.upper(),
                    "keyword": keyword,

                    "detected": analysis.get(
                        "detected",
                        False,
                    ),

                    "polarity": analysis.get(
                        "polarity"
                    ),

                    "uncertainty": analysis.get(
                        "uncertainty"
                    ),

                    "context": analysis.get(
                        "context"
                    ),

                    "confidence": analysis.get(
                        "confidence",
                        0.0,
                    ),

                    "negation_found": analysis.get(
                        "negation_found",
                        False,
                    ),

                    "uncertainty_found": analysis.get(
                        "uncertainty_found",
                        False,
                    ),

                    "context_text": analysis.get(
                        "context_text",
                        "",
                    ),

                    "action": "unknown",
                }

                # ------------------------------------------------------
                # ANALYZER DID NOT DETECT
                # ------------------------------------------------------

                if not analysis.get("detected", False):

                    check_result["action"] = (
                        "skipped_not_detected"
                    )

                    debug_info["checks"].append(
                        check_result
                    )

                    continue

                # ------------------------------------------------------
                # NEGATIVE CONDITION
                # ------------------------------------------------------

                if analysis.get("polarity") == "NEGATIVE":

                    check_result["action"] = (
                        "skipped_negative"
                    )

                    debug_info["checks"].append(
                        check_result
                    )

                    # Explicitly denied condition must not become
                    # an active critical condition.
                    continue

                # ------------------------------------------------------
                # PREVIOUS / HISTORICAL CONDITION
                # ------------------------------------------------------

                if analysis.get("context") == "PREVIOUS":

                    check_result["action"] = (
                        "skipped_previous"
                    )

                    debug_info["checks"].append(
                        check_result
                    )

                    # Historical condition is preserved in debug
                    # information but not treated as active.
                    continue

                # ------------------------------------------------------
                # SEMANTIC STATE
                # ------------------------------------------------------

                polarity = analysis.get(
                    "polarity",
                    "POSITIVE",
                )

                uncertainty = analysis.get(
                    "uncertainty"
                )

                confidence = analysis.get(
                    "confidence",
                    0.8,
                )

                # ------------------------------------------------------
                # SEVERITY
                # ------------------------------------------------------

                severity = config["severity"]

                # ------------------------------------------------------
                # UNCERTAIN CRITICAL CONDITION
                # ------------------------------------------------------

                if uncertainty == "HIGH":

                    # We DO NOT discard the condition.

                    # We reduce operational severity by one level
                    # only where appropriate.

                    if severity == "CRITICAL":
                        severity = "HIGH"

                    elif severity == "HIGH":
                        severity = "MEDIUM"

                    check_result["action"] = (
                        "added_uncertain"
                    )

                # ------------------------------------------------------
                # CONFIRMED / POSITIVE CONDITION
                # ------------------------------------------------------

                else:

                    check_result["action"] = (
                        "added_active"
                    )

                # ------------------------------------------------------
                # CONTEXT
                # ------------------------------------------------------

                context_type = analysis.get(
                    "context"
                )

                # ------------------------------------------------------
                # CONTEXT SNIPPET
                # ------------------------------------------------------

                position = text_lower.find(
                    keyword_lower
                )

                start = max(
                    0,
                    position - 30,
                )

                end = min(
                    len(text),
                    position + len(keyword) + 50,
                )

                context = text[
                    start:end
                ].strip()

                # ------------------------------------------------------
                # CONDITION RECORD
                # ------------------------------------------------------

                condition = {

                    "condition":
                        condition_type.upper(),

                    "severity":
                        severity,

                    "keyword":
                        keyword,

                    "context":
                        context,

                    "polarity":
                        polarity,

                    "confidence":
                        confidence,

                    "uncertainty":
                        uncertainty,

                    "context_type":
                        context_type,

                    "negation_found":
                        analysis.get(
                            "negation_found",
                            False,
                        ),

                    "uncertainty_found":
                        analysis.get(
                            "uncertainty_found",
                            False,
                        ),

                    "semantic_context":
                        analysis.get(
                            "context_text",
                            context,
                        ),

                    "timestamp":
                        self._utc_timestamp(),

                    "source":
                        "INCIDENT_INPUT",

                    "status":
                        "ACTIVE",
                }

                conditions.append(condition)

                # ------------------------------------------------------
                # STORE DEBUG
                # ------------------------------------------------------

                debug_info["checks"].append(
                    check_result
                )

                debug_info[
                    "keyword_results"
                ][keyword] = condition

                # Only one keyword per condition type.
                break

        return conditions, debug_info

    # ------------------------------------------------------------------
    # SEMANTIC SUMMARY
    # ------------------------------------------------------------------

    def _build_semantic_summary(
        self,
        conditions: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Build semantic summary.

        The summary preserves:
            - polarity distribution
            - uncertainty distribution
            - confidence
            - negation presence
            - uncertainty presence
        """

        if not conditions:

            return {
                "total_conditions": 0,
                "polarities": {},
                "uncertainties": [],
                "contexts": {},
                "average_confidence": 0.0,
                "has_negation": False,
                "has_uncertainty": False,
            }

        polarities: Dict[str, int] = {}

        uncertainties: List[str] = []

        contexts: Dict[str, int] = {}

        total_confidence = 0.0

        for condition in conditions:

            polarity = condition.get(
                "polarity",
                "UNKNOWN",
            )

            polarities[polarity] = (
                polarities.get(
                    polarity,
                    0,
                ) + 1
            )

            uncertainty = condition.get(
                "uncertainty"
            )

            if uncertainty:
                uncertainties.append(
                    uncertainty
                )

            context_type = condition.get(
                "context_type"
            )

            if context_type:

                contexts[context_type] = (
                    contexts.get(
                        context_type,
                        0,
                    ) + 1
                )

            total_confidence += condition.get(
                "confidence",
                0.8,
            )

        average_confidence = (
            total_confidence /
            len(conditions)
        )

        return {

            "total_conditions":
                len(conditions),

            "polarities":
                polarities,

            "uncertainties":
                uncertainties,

            "contexts":
                contexts,

            "average_confidence":
                round(
                    average_confidence,
                    3,
                ),

            "has_negation":
                polarities.get(
                    "NEGATIVE",
                    0,
                ) > 0,

            "has_uncertainty":
                len(uncertainties) > 0,
        }

    # ------------------------------------------------------------------
    # EVENT TYPE
    # ------------------------------------------------------------------

    def _determine_event_type(
        self,
        conditions: List[Dict[str, Any]],
    ) -> str:
        """
        Determine primary event type.

        Priority:
            1. CRITICAL
            2. HIGH
            3. MEDIUM
            4. first available condition
            5. GENERAL
        """

        if not conditions:
            return "GENERAL"

        for condition in conditions:

            if condition.get(
                "severity"
            ) == "CRITICAL":

                return condition[
                    "condition"
                ]

        for condition in conditions:

            if condition.get(
                "severity"
            ) == "HIGH":

                return condition[
                    "condition"
                ]

        for condition in conditions:

            if condition.get(
                "severity"
            ) == "MEDIUM":

                return condition[
                    "condition"
                ]

        return conditions[0][
            "condition"
        ]

    # ------------------------------------------------------------------
    # OVERALL SEVERITY
    # ------------------------------------------------------------------

    def _determine_overall_severity(
        self,
        conditions: List[Dict[str, Any]],
    ) -> str:
        """
        Determine overall event severity.
        """

        if any(
            c.get("severity") == "CRITICAL"
            for c in conditions
        ):
            return "CRITICAL"

        if any(
            c.get("severity") == "HIGH"
            for c in conditions
        ):
            return "HIGH"

        if any(
            c.get("severity") == "MEDIUM"
            for c in conditions
        ):
            return "MEDIUM"

        if conditions:
            return "LOW"

        return "LOW"

    # ------------------------------------------------------------------
    # UTC TIMESTAMP
    # ------------------------------------------------------------------

    @staticmethod
    def _utc_timestamp() -> str:
        """
        Return ISO-8601 UTC timestamp.
        """

        return (
            datetime.now(timezone.utc)
            .isoformat()
            .replace(
                "+00:00",
                "Z",
            )
        )

    # ------------------------------------------------------------------
    # PUBLIC ACCESSORS
    # ------------------------------------------------------------------

    def get_critical_conditions(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Return latest extracted critical conditions.
        """

        return self.critical_conditions

    def get_last_debug(
        self,
    ) -> Dict[str, Any]:
        """
        Return latest semantic debug information.
        """

        return self.last_debug
```
