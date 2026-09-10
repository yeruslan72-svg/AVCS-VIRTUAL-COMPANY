"""
AVCS VIRTUAL COMPANY
Aggregator — Consolidated Operational State

FUNCTION:
- Receive outputs from functional Dpts.
- Construct a consolidated operational state
- Preserve evidence, conflicts, recommendations, uncertainty
- Preserve structural fields from Constitution-compliant departments
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class Aggregator:
    """
    Aggregator constructs a consolidated operational state from Department outputs.

    Responsibilities:
    - Collect Department assessments
    - Synthesize evidence
    - Identify conflicts
    - Preserve uncertainty
    - Preserve structural fields (North, stability, reality, decision, coherence)
    - Build consolidated state
    """

    STRUCTURAL_FIELDS = [
        "north_status",
        "veto",
        "stability_status",
        "load_level",
        "reality_status",
        "reality_confidence",
        "facts",
        "unknowns",
        "contradictions",
        "decision",
        "decision_state",
        "structural_coherence",
        "role_integrity",
        "north_integrity",
        "decision_quality",
        "course",
        "course_state",
        "signal_state",
        "trajectory",
    ]

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.aggregation_log = []

    def aggregate(self, department_results: Dict[str, Any], event_id: str) -> Dict[str, Any]:
        """
        Aggregate Department results into a consolidated operational state.
        """
        self._log(f"Aggregating results for event: {event_id}")

        assessments: Dict[str, Any] = {}
        evidence: List[Any] = []
        recommendations: List[Any] = []
        uncertainty: List[Any] = []
        constraints: List[Any] = []
        conflicts: List[Dict[str, Any]] = []
        confidence_scores: List[float] = []
        structural: Dict[str, Any] = {}

        for dept_name, result in department_results.items():
            if not isinstance(result, dict):
                continue
            if "error" in result:
                continue

            assessments[dept_name] = result.get("assessment", "Unknown")
            evidence.extend(result.get("evidence", []) or [])
            recommendations.extend(result.get("recommendations", []) or [])
            uncertainty.extend(result.get("uncertainty", []) or [])
            constraints.extend(result.get("constraints", []) or [])

            if result.get("confidence") is not None:
                confidence_scores.append(result.get("confidence"))

            if result.get("conflict") or result.get("conflicts"):
                conflicts.append({
                    "department": dept_name,
                    "conflict": result.get("conflict") or result.get("conflicts"),
                })

            for field in self.STRUCTURAL_FIELDS:
                if field in result and result[field] is not None:
                    structural[field] = result[field]

        overall_confidence = None
        if confidence_scores:
            overall_confidence = sum(confidence_scores) / len(confidence_scores)

        has_conflict = len(conflicts) > 0

        operational_state: Dict[str, Any] = {
            "event_id": event_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "assessments": assessments,
            "evidence": list(dict.fromkeys(evidence)),
            "recommendations": list(dict.fromkeys(recommendations)),
            "uncertainty": list(dict.fromkeys(uncertainty)),
            "constraints": list(dict.fromkeys(constraints)),
            "conflicts": conflicts,
            "has_conflict": has_conflict,
            "overall_confidence": overall_confidence,
            "department_count": len(department_results),
            "successful_count": len(
                [r for r in department_results.values() if isinstance(r, dict) and "error" not in r]
            ),
            "status": "CONSOLIDATED",
        }

        if structural:
            operational_state["structural"] = structural

        self.aggregation_log.append(operational_state)
        return operational_state

    def _log(self, message: str, level: str = "INFO"):
        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[{timestamp}] [AGGREGATOR] [{level}] {message}")

    def get_aggregation_log(self) -> List[Dict[str, Any]]:
        return self.aggregation_log
