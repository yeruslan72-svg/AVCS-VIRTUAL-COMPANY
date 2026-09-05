"""
AVCS VIRTUAL COMPANY
NAVIGATOR Dpt. — Threat and Situation Assessment

CONTRACT:
PURPOSE: Assess operational situation and determine potential threat, consequence, and need for intervention
AUTHORITY: NONE
PROHIBITED: Authorize intervention, issue execution commands, override human authority
"""

from typing import Dict, Any, List
from datetime import datetime
from core.departments.base import BaseDepartment


class NavigatorDepartment(BaseDepartment):
    """
    NAVIGATOR Dpt. — Threat and Situation Assessment.
    
    Responsibilities:
    - Assess the developing situation
    - Identify potential threats
    - Project consequences
    - Assess time-to-event
    - Determine whether intervention appears operationally necessary
    - Identify decision dependencies
    - Evaluate available response requirements
    """

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("NAVIGATOR Dpt.", config)
        self.authority_state = "NO_AUTHORITY"

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming data and assess threat/situation.
        
        Required input fields:
        - situation: Description of the situation
        - time_to_event: Estimated time to potential impact (minutes)
        """
        # Validate input
        required_fields = ["situation", "time_to_event"]
        if not self._validate_input(input_data, required_fields):
            self._log("Missing required fields in input", "WARNING")
            return self._create_response(
                assessment="INVALID INPUT — Missing required fields",
                evidence=[],
                confidence=0.0,
                uncertainty=["Required fields: situation, time_to_event"],
                status="FAILED"
            )

        # Extract data
        situation = input_data.get("situation")
        time_to_event = input_data.get("time_to_event")
        confidence_level = input_data.get("confidence", 0.7)
        additional_evidence = input_data.get("evidence", [])

        # Generate event ID if not provided
        self.event_id = input_data.get("event_id") or self._generate_event_id()

        self._log(f"Processing threat assessment: {situation} (time: {time_to_event} min)")

        # Build evidence
        evidence = [
            f"Situation: {situation}",
            f"Time to event: {time_to_event} minutes",
            f"Assessment time: {datetime.utcnow().isoformat()}Z"
        ]
        if additional_evidence:
            evidence.extend(additional_evidence)

        # Determine threat level based on time to event
        threat_level = "LOW"
        if time_to_event <= 5:
            threat_level = "CRITICAL"
        elif time_to_event <= 15:
            threat_level = "HIGH"
        elif time_to_event <= 30:
            threat_level = "MEDIUM"
        
        # Determine intervention requirement
        intervention_required = False
        if threat_level in ["CRITICAL", "HIGH"]:
            intervention_required = True

        # Build uncertainty
        uncertainty = []
        if not input_data.get("intent"):
            uncertainty.append("Intent unknown")
        if not input_data.get("origin"):
            uncertainty.append("Origin unknown")
        if confidence_level < 0.8:
            uncertainty.append(f"Confidence level: {confidence_level:.2f}")

        # Build recommendations
        recommendations = []
        if intervention_required:
            recommendations.append(f"Intervention required: {threat_level} threat")
            recommendations.append("Escalate immediately")
        elif threat_level == "MEDIUM":
            recommendations.append("Monitor closely")
            recommendations.append("Prepare for possible intervention")
        else:
            recommendations.append("Continue monitoring")

        return self._create_response(
            assessment=f"Threat assessment: {threat_level} — {situation}",
            evidence=evidence,
            confidence=confidence_level,
            uncertainty=uncertainty,
            constraints=[],
            recommendations=recommendations,
            status="COMPLETED",
            event_id=self.event_id,
            threat_level=threat_level,
            intervention_required=intervention_required,
            time_to_event=time_to_event
        )

    def get_contract(self) -> Dict[str, Any]:
        """Return the NAVIGATOR Dpt. contract."""
        return {
            "department": self.department_name,
            "purpose": "Assess operational situation and determine potential threat, consequence, and need for intervention",
            "authority": self.authority_state,
            "prohibited_decisions": [
                "authorize intervention",
                "issue execution commands",
                "directly control HELM",
                "override human authority",
                "represent recommendation as authorization"
            ],
            "permitted_recommendations": [
                "intervention",
                "continued monitoring",
                "additional assessment",
                "escalation",
                "consideration of specified response options"
            ]
        }
