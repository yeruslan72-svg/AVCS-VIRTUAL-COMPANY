"""
AVCS VIRTUAL COMPANY
COMPASS Dpt. — Action and Trajectory Recommendation

CONTRACT:
PURPOSE: Develop operational response options and calculate/recommend appropriate trajectory or action parameters
AUTHORITY: NONE
PROHIBITED: Authorize response, issue command, bypass CAPTAIN Dpt.
"""

from typing import Dict, Any, List
from datetime import datetime
from core.departments.base import BaseDepartment


class CompassDepartment(BaseDepartment):
    """
    COMPASS Dpt. — Action and Trajectory Recommendation.
    
    Responsibilities:
    - Calculate response options
    - Evaluate trajectories
    - Calculate separation
    - Identify feasible headings
    - Compare response alternatives
    - Recommend a specific operational response
    """

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("COMPASS Dpt.", config)
        self.authority_state = "NO_AUTHORITY"

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming data and recommend action/trajectory.
        
        Required input fields:
        - current_heading: Current heading (degrees)
        - current_speed: Current speed (knots)
        - threat_heading: Threat heading (degrees)
        - threat_speed: Threat speed (knots)
        - separation_required: Required separation (nautical miles)
        """
        # Validate input
        required_fields = ["current_heading", "current_speed", "threat_heading", "threat_speed", "separation_required"]
        if not self._validate_input(input_data, required_fields):
            self._log("Missing required fields in input", "WARNING")
            return self._create_response(
                assessment="INVALID INPUT — Missing required fields",
                evidence=[],
                confidence=0.0,
                uncertainty=["Required fields: current_heading, current_speed, threat_heading, threat_speed, separation_required"],
                status="FAILED"
            )

        # Extract data
        current_heading = input_data.get("current_heading")
        current_speed = input_data.get("current_speed")
        threat_heading = input_data.get("threat_heading")
        threat_speed = input_data.get("threat_speed")
        separation_required = input_data.get("separation_required")

        # Generate event ID if not provided
        self.event_id = input_data.get("event_id") or self._generate_event_id()

        self._log(f"Processing compass calculation: heading={current_heading}°, speed={current_speed} kts")

        # Calculate recommended heading
        recommended_heading = current_heading
        separation_achieved = 0.0

        # Simple collision avoidance calculation
        # If threat is on a collision course, recommend turning away
        if abs(current_heading - threat_heading) < 30:
            # Turn 90 degrees away from threat
            recommended_heading = (current_heading + 90) % 360
            separation_achieved = 0.8  # Simulated separation in NM
        elif abs(current_heading - threat_heading) < 90:
            # Turn 45 degrees away
            recommended_heading = (current_heading + 45) % 360
            separation_achieved = 0.5
        else:
            # No immediate collision risk
            separation_achieved = 1.0

        # Build evidence
        evidence = [
            f"Current heading: {current_heading}°",
            f"Current speed: {current_speed} kts",
            f"Threat heading: {threat_heading}°",
            f"Threat speed: {threat_speed} kts",
            f"Required separation: {separation_required} NM",
            f"Recommended heading: {recommended_heading}°",
            f"Achieved separation: {separation_achieved:.1f} NM"
        ]

        # Build uncertainty
        uncertainty = []
        if separation_achieved < separation_required:
            uncertainty.append(f"Achieved separation {separation_achieved:.1f} NM < required {separation_required} NM")

        # Build recommendations
        recommendations = []
        if recommended_heading != current_heading:
            recommendations.append(f"Change heading to {recommended_heading}°")
            if separation_achieved >= separation_required:
                recommendations.append("Safe separation achieved")
            else:
                recommendations.append("Separation margin below requirement")
        else:
            recommendations.append("Maintain current heading")

        return self._create_response(
            assessment=f"Action recommendation: heading {recommended_heading}°",
            evidence=evidence,
            confidence=0.85 if separation_achieved >= separation_required else 0.70,
            uncertainty=uncertainty,
            constraints=[],
            recommendations=recommendations,
            status="COMPLETED",
            event_id=self.event_id,
            recommended_heading=recommended_heading,
            separation_achieved=separation_achieved,
            separation_required=separation_required
        )

    def get_contract(self) -> Dict[str, Any]:
        """Return the COMPASS Dpt. contract."""
        return {
            "department": self.department_name,
            "purpose": "Develop operational response options and calculate/recommend appropriate trajectory or action parameters",
            "authority": self.authority_state,
            "prohibited_decisions": [
                "authorize the response",
                "issue the command",
                "directly control HELM",
                "bypass CAPTAIN Dpt.",
                "convert recommendation into execution"
            ],
            "permitted_recommendations": [
                "heading",
                "course",
                "trajectory",
                "separation strategy",
                "speed adjustment",
                "alternative response options"
            ]
        }
