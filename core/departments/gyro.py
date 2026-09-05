"""
AVCS VIRTUAL COMPANY
GYRO Dpt. — Motion and Tracking Assessment

CONTRACT:
PURPOSE: Establish movement, heading, tracking, trajectory, and motion-related evidence
AUTHORITY: NONE
PROHIBITED: Authorize maneuver, issue commands, determine final threat
"""

from typing import Dict, Any, List
from datetime import datetime
from core.departments.base import BaseDepartment


class GyroDepartment(BaseDepartment):
    """
    GYRO Dpt. — Motion and Tracking Assessment.
    
    Responsibilities:
    - Establish current heading
    - Analyze movement
    - Establish trajectory
    - Identify changes in motion
    - Calculate relevant movement parameters
    - Detect deviations from expected movement
    """

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("GYRO Dpt.", config)
        self.authority_state = "NO_AUTHORITY"

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming data and assess motion/tracking.
        
        Required input fields:
        - heading: Current heading (degrees)
        - speed: Current speed (knots)
        - position: Current position
        """
        # Validate input
        required_fields = ["heading", "speed", "position"]
        if not self._validate_input(input_data, required_fields):
            self._log("Missing required fields in input", "WARNING")
            return self._create_response(
                assessment="INVALID INPUT — Missing required fields",
                evidence=[],
                confidence=0.0,
                uncertainty=["Required fields: heading, speed, position"],
                status="FAILED"
            )

        # Extract data
        heading = input_data.get("heading")
        speed = input_data.get("speed")
        position = input_data.get("position")
        track_history = input_data.get("track_history", [])

        # Generate event ID if not provided
        self.event_id = input_data.get("event_id") or self._generate_event_id()

        self._log(f"Processing motion assessment: heading={heading}°, speed={speed} kts")

        # Build evidence
        evidence = [
            f"Current heading: {heading}°",
            f"Current speed: {speed} knots",
            f"Current position: {position}",
            f"Assessment time: {datetime.utcnow().isoformat()}Z"
        ]
        if track_history:
            evidence.append(f"Track history: {len(track_history)} points")

        # Detect deviations
        deviations = []
        expected_heading = input_data.get("expected_heading")
        expected_speed = input_data.get("expected_speed")
        
        if expected_heading and abs(heading - expected_heading) > 5:
            deviations.append(f"Heading deviation: {heading - expected_heading}° from expected")
        if expected_speed and abs(speed - expected_speed) > 2:
            deviations.append(f"Speed deviation: {speed - expected_speed} kts from expected")

        # Build uncertainty
        uncertainty = []
        if not track_history:
            uncertainty.append("No track history available")
        if not input_data.get("trajectory"):
            uncertainty.append("Trajectory not established")

        # Build recommendations
        recommendations = []
        if deviations:
            recommendations.append(f"Verify: {', '.join(deviations)}")
        if not track_history:
            recommendations.append("Establish track history")
        if not recommendations:
            recommendations.append("Continue tracking")

        # Determine stability status
        stability = "STABLE"
        if deviations:
            stability = "CONDITIONALLY STABLE"
        if len(deviations) > 2:
            stability = "UNSTABLE"

        return self._create_response(
            assessment=f"Motion assessment completed: heading={heading}°, speed={speed} kts",
            evidence=evidence,
            confidence=0.85 if not deviations else 0.70,
            uncertainty=uncertainty,
            constraints=[],
            recommendations=recommendations,
            status="COMPLETED",
            event_id=self.event_id,
            heading=heading,
            speed=speed,
            deviations=deviations,
            stability=stability
        )

    def get_contract(self) -> Dict[str, Any]:
        """Return the GYRO Dpt. contract."""
        return {
            "department": self.department_name,
            "purpose": "Establish movement, heading, tracking, trajectory, and motion-related evidence",
            "authority": self.authority_state,
            "prohibited_decisions": [
                "authorize maneuver",
                "issue commands",
                "determine final threat",
                "authorize intervention",
                "alter operational objectives"
            ],
            "permitted_recommendations": [
                "continued tracking",
                "trajectory monitoring",
                "verification of unexpected movement",
                "recalculation where data quality changes"
            ]
        }
