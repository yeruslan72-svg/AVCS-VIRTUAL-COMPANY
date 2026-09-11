"""
AVCS VIRTUAL COMPANY
Aggregator — Consolidated Operational State

FUNCTION:
- Receive outputs from functional Dpts.
- Construct a consolidated operational state
- Preserve evidence, conflicts, recommendations, uncertainty
- Preserve structural fields from Constitution-compliant departments
- Preserve risk_assessment for DecisionEngine
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone


class Aggregator:
    """
    Aggregator constructs a consolidated operational state from Department outputs.
    """

    STRUCTURAL_FIELDS = [
        # COMPASS
        "north_status", "veto",
        # GYRO
        "stability_status", "load_level",
        # CHARTS
        "reality_status", "reality_confidence",
        "facts", "unknowns", "contradictions",
        # HELM
        "decision", "decision_state",
        # CAPTAIN
        "structural_coherence", "role_integrity",
        "north_integrity", "decision_quality",
        # NAVIGATOR
        "course", "course_state",
        # LOOKOUT
        "signal_state", "trajectory",
    ]

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.aggregation_log: List[Dict[str, Any]] = []

    def aggregate(
        self,
        department_results: Dict[str, Any],
        event_id: str
    ) -> Dict[str, Any]:
        self._log(f"Aggregating results for event: {event_id}")

        assessments: Dict[str, Any] = {}
        evidence: List[Any] = []
        recommendations: List[Any] = []
        uncertainty: List[Any] = []
        constraints: List[Any] = []
        conflicts: List[Dict[str, Any]] = []
        confidence_scores: List[float] = []
        structural: Dict[str, Any] = {}

        # Risk assessment (built from structural + evidence)
        risk_assessment: Dict[str, Any] = {
            "overall_risk": "LOW",
            "risks": [],
        }

        for dept_name, result in department_results.items():
            if not isinstance(result, dict):
                self._log(
                    f"Department {dept_name} returned non-dict result: {type(result)}",
                    level="WARNING"
                )
                continue
            if "error" in result:
                self._log(
                    f"Department {dept_name} returned error: {result['error']}",
                    level="WARNING"
                )
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

            # Collect risks
            for risk in result.get("risk_factors", []) or []:
                risk_assessment["risks"].append(risk)

        # Determine overall_risk from structural + risks
        risk_assessment["overall_risk"] = self._determine_overall_risk(
            structural, risk_assessment["risks"]
        )

        # Determine overall confidence
        overall_confidence = None
        if confidence_scores:
            overall_confidence = sum(confidence_scores) / len(confidence_scores)

        has_conflict = len(conflicts) > 0

        operational_state: Dict[str, Any] = {
            "event_id": event_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "assessments": assessments,
            "evidence": list(dict.fromkeys(evidence)),
            "recommendations": list(dict.fromkeys(recommendations)),
            "uncertainty": list(dict.fromkeys(uncertainty)),
            "constraints": list(dict.fromkeys(constraints)),
            "conflicts": conflicts,
            "has_conflict": has_conflict,
            "overall_confidence": overall_confidence,
            "department_count": len(department_results),
            "successful_count": len([
                r for r in department_results.values()
                if isinstance(r, dict) and "error" not in r
            ]),
            "risk_assessment": risk_assessment,
            "status": "CONSOLIDATED",
        }

        if structural:
            operational_state["structural"] = structural

        self.aggregation_log.append(operational_state)
        return operational_state

    def _determine_overall_risk(
        self,
        structural: Dict[str, Any],
        risks: List[Any]
    ) -> str:
        """
        Determine overall risk from structural fields and explicit risks.
        """
        # Structural conditions override
        if structural.get("veto") or structural.get("north_status") == "OUTSIDE NORTH":
            return "CRITICAL"
        if structural.get("stability_status") == "UNSTABLE":
            return "CRITICAL"
        if structural.get("reality_status") == "CONTRADICTORY":
            return "HIGH"
        if structural.get("decision_state") == "NO_DECISION":
            return "HIGH"

        # Explicit risks
        if len(risks) >= 3:
            return "HIGH"
        if len(risks) >= 1:
            return "MEDIUM"

        return "LOW"

    def _log(self, message: str, level: str = "INFO") -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        print(f"[{timestamp}] [AGGREGATOR] [{level}] {message}")

    def get_aggregation_log(self) -> List[Dict[str, Any]]:
        return self.aggregation_log
