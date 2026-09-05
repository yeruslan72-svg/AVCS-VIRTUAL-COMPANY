"""
AVCS VIRTUAL COMPANY
Decision Engine — Decision Proposal Generator

FUNCTION:
- Convert aggregated operational state into a structured Decision Proposal
- Identify: operational state, evidence, risks, recommendations, available actions, constraints, conflicts, authority requirement
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class DecisionEngine:
    """
    Decision Engine converts aggregated state into Decision Proposal.
    
    Responsibilities:
    - Analyze aggregated state
    - Generate decision options
    - Identify authority requirements
    - Formulate Decision Proposal
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.decision_log = []

    def formulate(self, aggregated_state: Dict[str, Any], conflict_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formulate a Decision Proposal from aggregated state and conflict result.
        
        Args:
            aggregated_state: Consolidated operational state
            conflict_result: Conflict detection result
            
        Returns:
            Decision Proposal
        """
        event_id = aggregated_state.get("event_id", "UNKNOWN")
        self._log(f"Formulating decision proposal for event: {event_id}")

        # Extract data
        assessments = aggregated_state.get("assessments", {})
        evidence = aggregated_state.get("evidence", [])
        recommendations = aggregated_state.get("recommendations", [])
        uncertainty = aggregated_state.get("uncertainty", [])
        constraints = aggregated_state.get("constraints", [])
        has_conflict = conflict_result.get("has_conflicts", False)
        decision_blocked = conflict_result.get("decision_blocked", False)
        conflicts = conflict_result.get("conflicts", [])

        # Determine decision options
        options = []
        if not decision_blocked:
            for rec in recommendations:
                if "continue" in rec.lower():
                    options.append({
                        "action": "CONTINUE",
                        "description": rec,
                        "risk": "LOW"
                    })
                elif "change" in rec.lower() or "heading" in rec.lower():
                    options.append({
                        "action": "CHANGE_COURSE",
                        "description": rec,
                        "risk": "MEDIUM"
                    })
                elif "stop" in rec.lower() or "intervention" in rec.lower():
                    options.append({
                        "action": "STOP_INTERVENTION",
                        "description": rec,
                        "risk": "HIGH"
                    })
                elif "monitor" in rec.lower():
                    options.append({
                        "action": "MONITOR",
                        "description": rec,
                        "risk": "LOW"
                    })
        else:
            options.append({
                "action": "BLOCKED",
                "description": "Decision blocked due to conflicts",
                "risk": "HIGH"
            })

        # Determine authority requirement
        authority_required = "CAPTAIN Dpt."
        if not options:
            authority_required = "ESCALATE"

        # Determine recommended action
        recommended_action = None
        if options and not decision_blocked:
            # Prefer CHANGE_COURSE or STOP_INTERVENTION for threats
            for opt in options:
                if opt["action"] in ["CHANGE_COURSE", "STOP_INTERVENTION"]:
                    recommended_action = opt
                    break
            if not recommended_action:
                recommended_action = options[0]

        # Build Decision Proposal
        decision_proposal = {
            "event_id": event_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "operational_state": {
                "assessments": assessments,
                "constraints": constraints,
                "uncertainty": uncertainty
            },
            "evidence": evidence,
            "risks": [{
                "description": rec,
                "severity": "HIGH" if "intervention" in rec or "stop" in rec else "MEDIUM"
            } for rec in recommendations if "intervention" in rec or "stop" in rec or "change" in rec],
            "recommendations": recommendations,
            "available_options": options,
            "constraints": constraints,
            "conflicts": conflicts,
            "has_conflict": has_conflict,
            "decision_blocked": decision_blocked,
            "authority_required": authority_required,
            "proposed_action": recommended_action,
            "status": "PROPOSAL_READY"
        }

        # Log decision
        self.decision_log.append(decision_proposal)

        return decision_proposal

    def _log(self, message: str, level: str = "INFO"):
        """Simple logging for DecisionEngine."""
        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[{timestamp}] [DECISION_ENGINE] [{level}] {message}")

    def get_decision_log(self) -> List[Dict[str, Any]]:
        """Return the decision log."""
        return self.decision_log
