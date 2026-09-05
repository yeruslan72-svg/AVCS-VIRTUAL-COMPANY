"""
AVCS VIRTUAL COMPANY
CAPTAIN Dpt. — Decision Authority Interface

CONTRACT:
PURPOSE: Provide the decision-authority interface between the INS decision architecture and the authorized human decision-maker
AUTHORITY: HUMAN AUTHORITY INTERFACE
PROHIBITED: Silently convert AI recommendation into authorization, conceal unresolved conflicts, fabricate human authorization
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from core.departments.base import BaseDepartment


class CaptainDepartment(BaseDepartment):
    """
    CAPTAIN Dpt. — Decision Authority Interface.
    
    Responsibilities:
    - Assemble the decision state
    - Identify unresolved conflicts
    - Identify authority requirements
    - Present available options
    - Receive human authorization
    - Transmit authorized commands
    - Record the resulting authority transition
    - Initiate stand-down when conditions are satisfied
    """

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("CAPTAIN Dpt.", config)
        self.authority_state = "HUMAN_AUTHORITY_INTERFACE"
        self.decision_history = []
        self.authorization_status = "PENDING"

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming data and present decision state.
        
        Required input fields:
        - decision_proposal: Proposed decision
        - evidence: Supporting evidence
        - recommendations: Available recommendations
        - conflicts: Unresolved conflicts (if any)
        """
        # Validate input
        required_fields = ["decision_proposal", "evidence"]
        if not self._validate_input(input_data, required_fields):
            self._log("Missing required fields in input", "WARNING")
            return self._create_response(
                assessment="INVALID INPUT — Missing required fields",
                evidence=[],
                confidence=0.0,
                uncertainty=["Required fields: decision_proposal, evidence"],
                status="FAILED"
            )

        # Extract data
        decision_proposal = input_data.get("decision_proposal")
        evidence = input_data.get("evidence", [])
        recommendations = input_data.get("recommendations", [])
        conflicts = input_data.get("conflicts", [])
        human_authorization = input_data.get("human_authorization", None)
        available_options = input_data.get("available_options", [])

        # Generate event ID if not provided
        self.event_id = input_data.get("event_id") or self._generate_event_id()

        self._log(f"Processing decision state: proposal='{decision_proposal}', authorization={human_authorization}")

        # Determine authority status
        if human_authorization is None:
            authorization_status = "AWAITING_AUTHORITY"
        elif human_authorization is True:
            authorization_status = "AUTHORIZED"
        else:
            authorization_status = "REJECTED"

        # Build decision state
        decision_state = {
            "proposal": decision_proposal,
            "evidence": evidence,
            "recommendations": recommendations,
            "conflicts": conflicts,
            "available_options": available_options,
            "authorization_status": authorization_status,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        # Build evidence
        evidence_list = [
            f"Decision proposal: {decision_proposal}",
            f"Authorization status: {authorization_status}",
            f"Number of evidence items: {len(evidence)}",
            f"Number of recommendations: {len(recommendations)}",
            f"Conflicts: {len(conflicts)}"
        ]

        # Build uncertainty
        uncertainty = []
        if conflicts:
            uncertainty.append(f"Unresolved conflicts: {len(conflicts)}")
        if not available_options:
            uncertainty.append("No alternative options available")
        if authorization_status == "AWAITING_AUTHORITY":
            uncertainty.append("Awaiting human authorization")

        # Build recommendations
        recommendations_list = []
        if authorization_status == "AWAITING_AUTHORITY":
            recommendations_list.append("Human authorization required")
            recommendations_list.append("Consider available options")
        elif authorization_status == "AUTHORIZED":
            recommendations_list.append("Proceed with authorized action")
            if conflicts:
                recommendations_list.append("Review conflicts before execution")
        else:
            recommendations_list.append("Decision rejected — re-evaluate proposal")
            if conflicts:
                recommendations_list.append("Resolve conflicts before resubmission")

        # Record decision in history if authorized or rejected
        if human_authorization is not None:
            self.decision_history.append({
                "event_id": self.event_id,
                "proposal": decision_proposal,
                "authorized": human_authorization,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })

        return self._create_response(
            assessment=f"Decision state: {authorization_status}",
            evidence=evidence_list,
            confidence=0.95 if authorization_status != "AWAITING_AUTHORITY" else 0.50,
            uncertainty=uncertainty,
            constraints=[],
            recommendations=recommendations_list,
            status="COMPLETED",
            event_id=self.event_id,
            decision_state=decision_state,
            authorization_status=authorization_status,
            human_authorization=human_authorization,
            decision_proposal=decision_proposal,
            conflicts=conflicts,
            is_authorized=(authorization_status == "AUTHORIZED")
        )

    def get_contract(self) -> Dict[str, Any]:
        """Return the CAPTAIN Dpt. contract."""
        return {
            "department": self.department_name,
            "purpose": "Provide the decision-authority interface between the INS decision architecture and the authorized human decision-maker",
            "authority": "HUMAN_AUTHORITY_INTERFACE",
            "prohibited_decisions": [
                "silently convert an AI recommendation into authorization",
                "conceal unresolved conflicts",
                "fabricate human authorization",
                "represent a recommendation as a human decision",
                "authorize action without the required authority state"
            ],
            "permitted_recommendations": [
                "recommended action",
                "alternative actions",
                "continuation",
                "intervention",
                "request for additional information",
                "stand-down",
                "escalation"
            ]
        }

    def get_decision_history(self) -> List[Dict[str, Any]]:
        """Return the history of decisions."""
        return self.decision_history

    def get_authorization_status(self) -> str:
        """Return the current authorization status."""
        return self.authorization_status
