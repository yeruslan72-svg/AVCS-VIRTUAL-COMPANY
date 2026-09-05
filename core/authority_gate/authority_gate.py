"""
AVCS VIRTUAL COMPANY
Authority Gate — Authority Boundary Interface

FUNCTION:
- Establish boundary between what the system recommends and what the organization authorizes
- Distinguish between: information, analysis, recommendation, authorization, command, execution, result
- Maintain explicit authority boundary
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class AuthorityGate:
    """
    Authority Gate establishes the boundary between recommendation and authorization.
    
    Responsibilities:
    - Receive Decision Proposal
    - Present to human authority
    - Receive authorization
    - Distinguish recommendation from authorization
    - Record authority transition
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.authorization_log = []
        self.pending_decisions = []

    def present_decision(self, decision_proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Present decision proposal to authority gate.
        
        Args:
            decision_proposal: Decision Proposal from Decision Engine
            
        Returns:
            Decision state with authority status
        """
        event_id = decision_proposal.get("event_id", "UNKNOWN")
        self._log(f"Presenting decision for event: {event_id}")

        # Determine if authorization is required
        authority_required = decision_proposal.get("authority_required", "CAPTAIN Dpt.")
        proposed_action = decision_proposal.get("proposed_action")
        has_conflict = decision_proposal.get("has_conflict", False)
        decision_blocked = decision_proposal.get("decision_blocked", False)

        # If blocked by conflicts, require immediate escalation
        if decision_blocked:
            authority_status = "ESCALATION_REQUIRED"
            authority_message = "Decision blocked by conflicts — immediate human review required"
        elif has_conflict:
            authority_status = "AWAITING_AUTHORITY"
            authority_message = "Decision with conflicts — human authorization required"
        elif proposed_action:
            authority_status = "AWAITING_AUTHORITY"
            authority_message = f"Proposed action: {proposed_action.get('action', 'UNKNOWN')} — awaiting authorization"
        else:
            authority_status = "AWAITING_AUTHORITY"
            authority_message = "No clear proposed action — human guidance required"

        # Build authority state
        authority_state = {
            "event_id": event_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "authority_required": authority_required,
            "authority_status": authority_status,
            "authority_message": authority_message,
            "proposed_action": proposed_action,
            "decision_proposal": decision_proposal,
            "human_authorization": None,  # Will be set by human
            "is_blocked": decision_blocked,
            "has_conflict": has_conflict,
            "status": "PENDING"
        }

        self.pending_decisions.append(authority_state)

        return authority_state

    def authorize(self, event_id: str, authorized: bool, comments: Optional[str] = None) -> Dict[str, Any]:
        """
        Apply human authorization to a pending decision.
        
        Args:
            event_id: Event ID of the decision
            authorized: True to authorize, False to reject
            comments: Optional comments from human authority
            
        Returns:
            Authorization result
        """
        self._log(f"Applying authorization for event: {event_id}")

        # Find pending decision
        for decision in self.pending_decisions:
            if decision.get("event_id") == event_id:
                decision["human_authorization"] = authorized
                decision["authorization_comments"] = comments
                decision["authorization_timestamp"] = datetime.utcnow().isoformat() + "Z"
                decision["status"] = "AUTHORIZED" if authorized else "REJECTED"

                # Log authorization
                log_entry = {
                    "event_id": event_id,
                    "authorized": authorized,
                    "comments": comments,
                    "timestamp": decision["authorization_timestamp"],
                    "status": decision["status"]
                }
                self.authorization_log.append(log_entry)

                return {
                    "event_id": event_id,
                    "authorized": authorized,
                    "status": decision["status"],
                    "authorization_timestamp": decision["authorization_timestamp"],
                    "comments": comments,
                    "message": f"Decision {'authorized' if authorized else 'rejected'} by human authority"
                }

        return {
            "event_id": event_id,
            "authorized": False,
            "status": "NOT_FOUND",
            "message": "Decision not found in pending decisions"
        }

    def get_authorization_status(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get authorization status for an event."""
        for decision in self.pending_decisions:
            if decision.get("event_id") == event_id:
                return {
                    "event_id": event_id,
                    "authority_status": decision.get("authority_status"),
                    "human_authorization": decision.get("human_authorization"),
                    "status": decision.get("status")
                }
        return None

    def _log(self, message: str, level: str = "INFO"):
        """Simple logging for AuthorityGate."""
        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[{timestamp}] [AUTHORITY_GATE] [{level}] {message}")

    def get_authorization_log(self) -> List[Dict[str, Any]]:
        """Return the authorization log."""
        return self.authorization_log

    def get_pending_decisions(self) -> List[Dict[str, Any]]:
        """Return pending decisions."""
        return self.pending_decisions
