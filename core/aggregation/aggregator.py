"""
AVCS VIRTUAL COMPANY
Aggregator — Consolidated Operational State

FUNCTION:
- Receive outputs from functional Dpts.
- Construct a consolidated operational state
- Preserve evidence, conflicts, recommendations, uncertainty
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
    - Build consolidated state
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.aggregation_log = []

    def aggregate(self, department_results: Dict[str, Any], event_id: str) -> Dict[str, Any]:
        """
        Aggregate Department results into a consolidated operational state.
        
        Args:
            department_results: Dictionary of Department outputs
            event_id: Event ID for this aggregation
            
        Returns:
            Consolidated operational state
        """
        self._log(f"Aggregating results for event: {event_id}")

        # Extract all assessments
        assessments = {}
        evidence = []
        recommendations = []
        uncertainty = []
        constraints = []
        conflicts = []
        confidence_scores = []

        for dept_name, result in department_results.items():
            if "error" in result:
                continue

            assessments[dept_name] = result.get("assessment", "Unknown")
            evidence.extend(result.get("evidence", []))
            recommendations.extend(result.get("recommendations", []))
            uncertainty.extend(result.get("uncertainty", []))
            constraints.extend(result.get("constraints", []))
            if result.get("confidence") is not None:
                confidence_scores.append(result.get("confidence"))

            # Check for conflicts
            if "conflict" in result or result.get("conflicts"):
                conflicts.append({
                    "department": dept_name,
                    "conflict": result.get("conflict") or result.get("conflicts")
                })

        # Calculate overall confidence
        overall_confidence = None
        if confidence_scores:
            overall_confidence = sum(confidence_scores) / len(confidence_scores)

        # Determine if any conflict exists
        has_conflict = len(conflicts) > 0

        # Build operational state
        operational_state = {
            "event_id": event_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "assessments": assessments,
            "evidence": list(set(evidence)),  # Remove duplicates
            "recommendations": list(set(recommendations)),
            "uncertainty": list(set(uncertainty)),
            "constraints": list(set(constraints)),
            "conflicts": conflicts,
            "has_conflict": has_conflict,
            "overall_confidence": overall_confidence,
            "department_count": len(department_results),
            "successful_count": len([r for r in department_results.values() if "error" not in r]),
            "status": "CONSOLIDATED"
        }

        # Log aggregation
        self.aggregation_log.append(operational_state)

        return operational_state

    def _log(self, message: str, level: str = "INFO"):
        """Simple logging for Aggregator."""
        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[{timestamp}] [AGGREGATOR] [{level}] {message}")

    def get_aggregation_log(self) -> List[Dict[str, Any]]:
        """Return the aggregation log."""
        return self.aggregation_log
