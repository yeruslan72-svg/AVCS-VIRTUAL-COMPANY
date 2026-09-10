"""
AVCS VIRTUAL COMPANY
Authority Gate — Authority Boundary Interface

FUNCTION:
- Establish boundary between what the system recommends and what the organization authorizes
- Distinguish between: information, analysis, recommendation, authorization, command, execution, result
- Respect North boundary (veto)
- Preserve structural fields in authority state
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class AuthorityGate:
    """
    Authority Gate establishes the boundary between recommendation and authorization.

    Responsibilities:
    - Receive Decision Proposal
    - Respect North boundary (COMPASS veto)
    - Present to human authority
    - Receive authorization
    - Distinguish recommendation from authorization
    - Record authority transition
    - Preserve structural fields
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

        # -------------------------------------------------------------------
        # Extract structural fields from decision proposal
        # -------------------------------------------------------------------

        structural = decision_proposal.get("structural", {})
        north_status = structural.get("north_status")
        veto = structural.get("veto", False)
        stability_status = structural.get("stability_status")
        reality_status = structural.get("reality_status")
        structural_coherence = structural.get("structural_coherence")

        proposal_status = decision_proposal.get("status", "PROPOSAL_READY")

        authority_required = decision_proposal.get("authority_required", "CAPTAIN Dpt.")
        proposed_action = decision_proposal.get("proposed_action")
        has_conflict = decision_proposal.get("has_conflict", False)
        decision_blocked = decision_proposal.get("decision_blocked", False)

        # -------------------------------------------------------------------
        # North boundary — non-negotiable
        # -------------------------------------------------------------------

        if veto or north_status == "OUTSIDE NORTH" or proposal_status == "OUTSIDE_NORTH":
            authority_status = "NORTH_VIOLATION"
            authority_message = (
                "Decision violates North — continuation prohibited. "
                "No authorization may override North."
            )
        elif north_status == "UNDETERMINED" or proposal_status == "NORTH_UNDETERMINED":
            authority_status = "NORTH_UNDETERMINED"
            authority_message = (
                "North not confirmed — requalification required before continuation."
            )
        elif stability_status == "UNSTABLE" or proposal_status == "UNSTABLE":
            authority_status = "STABILITY_HOLD"
            authority_message = (
                "Environment unstable — action not supported. "
                "Hold until stability is restored."
            )
        elif reality_status == "CONTRADICTORY" or proposal_status == "CONTRADICTORY":
            authority_status = "REALITY_HOLD"
            authority_message = (
                "Conflicting evidence — reality not established. "
                "Hold until contradictions are resolved."
            )
        elif decision_blocked or proposal_status == "BLOCKED":
            authority_status = "ESCALATION_REQUIRED"
            authority_message = (
                "Decision blocked by conflicts — immediate human review required."
            )
        elif has_conflict:
            authority_status = "AWAITING_AUTHORITY"
            authority_message = (
                "Decision with conflicts — human authorization required."
            )
        elif proposed_action:
            authority_status = "AWAITING_AUTHORITY"
            authority_message = (
                f"Proposed action: {proposed_action.get('action', 'UNKNOWN')} — "
                "awaiting authorization."
            )
        else:
            authority_status = "AWAITING_AUTHORITY"
            authority_message = (
                "No clear proposed action — human guidance required."
            )

        # -------------------------------------------------------------------
        # Build authority state
        # -------------------------------------------------------------------

        authority_state = {
            "event_id": event_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "authority_required": authority_required,
            "authority_status": authority_status,
            "authority_message": authority_message,
            "proposed_action": proposed_action,
            "decision_proposal": decision_proposal,
            "structural": {
                "north_status": north_status,
                "veto": veto,
                "stability_status": stability_status,
                "reality_status": reality_status,
                "structural_coherence": structural_coherence,
            },
            "human_authorization": None,  # Will be set by human
            "is_blocked": decision_blocked,
            "has_conflict": has_conflict,
            "status": "PENDING",
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

        for decision in self.pending_decisions:
            if decision.get("event_id") == event_id:
                # North may not be overridden by authorization
                structural = decision.get("structural", {})
                if structural.get("veto") or structural.get("north_status") == "OUTSIDE NORTH":
                    decision["human_authorization"] = False
                    decision["authorization_comments"] = (
                        "Authorization denied: North violation cannot be overridden."
                    )
                    decision["authorization_timestamp"] = datetime.utcnow().isoformat() + "Z"
                    decision["status"] = "NORTH_VIOLATION"

                    self.authorization_log.append({
                        "event_id": event_id,
                        "authorized": False,
                        "comments": decision["authorization_comments"],
                        "timestamp": decision["authorization_timestamp"],
                        "status": "NORTH_VIOLATION",
                    })

                    return {
                        "event_id": event_id,
                        "authorized": False,
                        "status": "NORTH_VIOLATION",
                        "authorization_timestamp": decision["authorization_timestamp"],
                        "comments": decision["authorization_comments"],
                        "message": "Authorization denied — North violation.",
                    }

                decision["human_authorization"] = authorized
                decision["authorization_comments"] = comments
                decision["authorization_timestamp"] = datetime.utcnow().isoformat() + "Z"
                decision["status"] = "AUTHORIZED" if authorized else "REJECTED"

                log_entry = {
                    "event_id": event_id,
                    "authorized": authorized,
                    "comments": comments,
                    "timestamp": decision["authorization_timestamp"],
                    "status": decision["status"],
                }
                self.authorization_log.append(log_entry)

                return {
                    "event_id": event_id,
                    "authorized": authorized,
                    "status": decision["status"],
                    "authorization_timestamp": decision["authorization_timestamp"],
                    "comments": comments,
                    "message": f"Decision {'authorized' if authorized else 'rejected'} by human authority.",
                }

        return {
            "event_id": event_id,
            "authorized": False,
            "status": "NOT_FOUND",
            "message": "Decision not found in pending decisions",
        }

    def get_authorization_status(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get authorization status for an event."""
        for decision in self.pending_decisions:
            if decision.get("event_id") == event_id:
                return {
                    "event_id": event_id,
                    "authority_status": decision.get("authority_status"),
                    "human_authorization": decision.get("human_authorization"),
                    "status": decision.get("status"),
                }
        return None

    def _log(self, message: str, level: str = "INFO"):
        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[{timestamp}] [AUTHORITY_GATE] [{level}] {message}")

    def get_authorization_log(self) -> List[Dict[str, Any]]:
        return self.authorization_log

    def get_pending_decisions(self) -> List[Dict[str, Any]]:
        return self.pending_decisions
