"""
AVCS VIRTUAL COMPANY
Conflict Detector — Conflict Identification and Preservation

FUNCTION:
- Identify conflicts between Department assessments
- Preserve conflicts for visibility
- Determine if conflicts block execution
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class ConflictDetector:
    """
    Conflict Detector identifies and preserves conflicts.
    
    Responsibilities:
    - Identify conflicts between assessments
    - Preserve conflict information
    - Determine if conflicts block execution
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.conflict_log = []

    def detect(self, aggregated_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect conflicts in the aggregated operational state.
        
        Args:
            aggregated_state: Consolidated operational state
            
        Returns:
            Conflict detection result
        """
        event_id = aggregated_state.get("event_id", "UNKNOWN")
        self._log(f"Detecting conflicts for event: {event_id}")

        assessments = aggregated_state.get("assessments", {})
        constraints = aggregated_state.get("constraints", [])
        recommendations = aggregated_state.get("recommendations", [])

        conflicts = []
        conflict_type = "NONE"
        decision_blocked = False

        # Check for conflicts between NAVIGATOR and HELM
        if "NAVIGATOR Dpt." in assessments and "HELM Dpt." in assessments:
            nav_assessment = assessments.get("NAVIGATOR Dpt.", "")
            helm_assessment = assessments.get("HELM Dpt.", "")

            if "intervention" in nav_assessment.lower() and "cannot" in helm_assessment.lower():
                conflicts.append({
                    "type": "NAVIGATOR_VS_HELM",
                    "description": "NAVIGATOR recommends intervention, HELM reports cannot execute",
                    "nav_assessment": nav_assessment,
                    "helm_assessment": helm_assessment,
                    "severity": "HIGH"
                })
                conflict_type = "HIGH"
                decision_blocked = True

        # Check for constraints conflicts
        if constraints:
            for constraint in constraints:
                if "cannot" in constraint.lower() or "not possible" in constraint.lower():
                    conflicts.append({
                        "type": "CONSTRAINT",
                        "description": f"Constraint: {constraint}",
                        "severity": "HIGH"
                    })
                    conflict_type = "HIGH"
                    decision_blocked = True

        # Check for recommendation conflicts
        if recommendations:
            # Check for conflicting recommendations
            for rec in recommendations:
                if "stop" in rec.lower() and "continue" in recommendations:
                    conflicts.append({
                        "type": "RECOMMENDATION_CONFLICT",
                        "description": "Conflicting recommendations: stop vs continue",
                        "severity": "MEDIUM"
                    })
                    conflict_type = "MEDIUM"

        # Build result
        result = {
            "event_id": event_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "conflicts": conflicts,
            "conflict_type": conflict_type,
            "decision_blocked": decision_blocked,
            "has_conflicts": len(conflicts) > 0,
            "status": "COMPLETED"
        }

        # Log conflicts
        self.conflict_log.append(result)

        return result

    def _log(self, message: str, level: str = "INFO"):
        """Simple logging for ConflictDetector."""
        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[{timestamp}] [CONFLICT_DETECTOR] [{level}] {message}")

    def get_conflict_log(self) -> List[Dict[str, Any]]:
        """Return the conflict log."""
        return self.conflict_log
