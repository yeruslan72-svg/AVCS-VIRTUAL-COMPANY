"""
AVCS VIRTUAL COMPANY
Conflict Detector — Structural Conflict Identification

FUNCTION:
- Identify STRUCTURAL conflicts between department outputs
- Preserve conflicts for visibility
- Determine if conflicts block execution

PRINCIPLE:
Conflict is a structural condition — not an error to be hidden.
Conflict detection must be structural, not textual.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone


class ConflictDetector:
    """
    Conflict Detector identifies structural conflicts between departments.

    A structural conflict exists when two departments return states
    that cannot both be true simultaneously.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.conflict_log: List[Dict[str, Any]] = []

    def detect(self, aggregated_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect structural conflicts in aggregated state.

        Returns:
            Conflict detection result with structural conflicts.
        """
        event_id = aggregated_state.get("event_id", "UNKNOWN")
        self._log(f"Detecting structural conflicts for event: {event_id}")

        structural = aggregated_state.get("structural", {})

        north_status = structural.get("north_status")
        veto = structural.get("veto", False)
        stability_status = structural.get("stability_status")
        reality_status = structural.get("reality_status")
        decision_state = structural.get("decision_state")
        course_state = structural.get("course_state")
        signal_state = structural.get("signal_state")
        structural_coherence = structural.get("structural_coherence")
        role_integrity = structural.get("role_integrity")
        north_integrity = structural.get("north_integrity")
        decision_quality = structural.get("decision_quality")

        conflicts: List[Dict[str, Any]] = []
        decision_blocked = False

        # -------------------------------------------------------------------
        # 1. NORTH VETO vs DECISION
        # If COMPASS vetoes North, no DECISION_MADE should exist.
        # -------------------------------------------------------------------
        if (veto or north_status == "OUTSIDE NORTH") and decision_state == "DECISION_MADE":
            conflicts.append({
                "type": "NORTH_VETO_VS_DECISION",
                "description": "COMPASS vetoed North, but HELM made a decision",
                "severity": "CRITICAL",
                "involved": ["COMPASS Dpt.", "HELM Dpt."],
            })
            decision_blocked = True

        # -------------------------------------------------------------------
        # 2. UNSTABLE ENVIRONMENT vs DECISION
        # If GYRO reports UNSTABLE, no DECISION_MADE should exist.
        # -------------------------------------------------------------------
        if stability_status == "UNSTABLE" and decision_state == "DECISION_MADE":
            conflicts.append({
                "type": "UNSTABLE_VS_DECISION",
                "description": "GYRO reports unstable environment, but HELM made a decision",
                "severity": "HIGH",
                "involved": ["GYRO Dpt.", "HELM Dpt."],
            })
            decision_blocked = True

        # -------------------------------------------------------------------
        # 3. CONTRADICTORY REALITY vs DECISION
        # If CHARTS reports CONTRADICTORY, no DECISION_MADE should exist.
        # -------------------------------------------------------------------
        if reality_status == "CONTRADICTORY" and decision_state == "DECISION_MADE":
            conflicts.append({
                "type": "CONTRADICTORY_VS_DECISION",
                "description": "CHARTS reports contradictory reality, but HELM made a decision",
                "severity": "HIGH",
                "involved": ["CHARTS Dpt.", "HELM Dpt."],
            })
            decision_blocked = True

        # -------------------------------------------------------------------
        # 4. COURSE PROPOSED vs OUTSIDE NORTH
        # NAVIGATOR should not propose course outside North.
        # -------------------------------------------------------------------
        if course_state in ("PROPOSED", "ADJUST") and (veto or north_status == "OUTSIDE NORTH"):
            conflicts.append({
                "type": "COURSE_VS_NORTH",
                "description": "NAVIGATOR proposed course, but COMPASS reports outside North",
                "severity": "CRITICAL",
                "involved": ["NAVIGATOR Dpt.", "COMPASS Dpt."],
            })
            decision_blocked = True

        # -------------------------------------------------------------------
        # 5. DEVIATION vs INTACT COHERENCE
        # If LOOKOUT indicates deviation, CAPTAIN should not report INTACT.
        # -------------------------------------------------------------------
        if signal_state == "DEVIATION_INDICATED" and structural_coherence == "INTACT":
            conflicts.append({
                "type": "DEVIATION_VS_COHERENCE",
                "description": "LOOKOUT indicates deviation, but CAPTAIN reports intact coherence",
                "severity": "MEDIUM",
                "involved": ["LOOKOUT Dpt.", "CAPTAIN Dpt."],
            })

        # -------------------------------------------------------------------
        # 6. NORTH INTEGRITY vs NORTH STATUS
        # If COMPASS says WITHIN NORTH but CAPTAIN says BROKEN → conflict.
        # -------------------------------------------------------------------
        if north_status == "WITHIN NORTH" and north_integrity == "BROKEN":
            conflicts.append({
                "type": "NORTH_STATUS_VS_INTEGRITY",
                "description": "COMPASS says WITHIN NORTH, but CAPTAIN says North integrity BROKEN",
                "severity": "HIGH",
                "involved": ["COMPASS Dpt.", "CAPTAIN Dpt."],
            })
            decision_blocked = True

        # -------------------------------------------------------------------
        # 7. ROLE INTEGRITY BROKEN
        # If CAPTAIN reports role integrity broken, that's a structural conflict.
        # -------------------------------------------------------------------
        if role_integrity == "BROKEN":
            conflicts.append({
                "type": "ROLE_INTEGRITY_BROKEN",
                "description": "CAPTAIN reports role integrity broken",
                "severity": "HIGH",
                "involved": ["CAPTAIN Dpt."],
            })
            decision_blocked = True

        # -------------------------------------------------------------------
        # Determine conflict type
        # -------------------------------------------------------------------
        if not conflicts:
            conflict_type = "NONE"
        elif any(c["severity"] == "CRITICAL" for c in conflicts):
            conflict_type = "CRITICAL"
        elif any(c["severity"] == "HIGH" for c in conflicts):
            conflict_type = "HIGH"
        else:
            conflict_type = "MEDIUM"

        result = {
            "event_id": event_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "conflicts": conflicts,
            "conflict_type": conflict_type,
            "decision_blocked": decision_blocked,
            "has_conflicts": len(conflicts) > 0,
            "status": "COMPLETED",
        }

        self.conflict_log.append(result)
        self._log(
            f"Conflicts detected: {len(conflicts)} "
            f"(type: {conflict_type}, blocked: {decision_blocked})"
        )
        return result

    def _log(self, message: str, level: str = "INFO") -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        print(f"[{timestamp}] [CONFLICT_DETECTOR] [{level}] {message}")

    def get_conflict_log(self) -> List[Dict[str, Any]]:
        return self.conflict_log
