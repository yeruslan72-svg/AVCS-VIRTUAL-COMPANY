"""
AVCS VIRTUAL COMPANY
Drone Scenario — Unidentified Drone Detection

FUNCTION:
- Define drone detection scenario
- Provide event data
- Test decision cycle
"""

from typing import Dict, Any
from datetime import datetime


class DroneScenario:
    """
    Drone Scenario for testing AVCS decision cycle.
    """

    @staticmethod
    def get_event_data() -> Dict[str, Any]:
        """Get drone detection event data."""
        return {
            "event_id": f"EVT-{datetime.utcnow().strftime('%Y%m%d')}-001",
            "object": "Unidentified Drone",
            "position": "1.2 NM, Bearing 270°",
            "heading": 90,
            "speed": 25,
            "altitude": 200,
            "threat_heading": 100,
            "threat_speed": 30,
            "separation_required": 0.5,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "observations": [
                "Object detected at 1.2 NM",
                "Bearing: 270° true",
                "Altitude: 200 ft",
                "Heading: 090°",
                "Speed: 25 knots",
                "No transponder signal",
                "No IFF response",
                "Not on filed flight plans",
                "Position within restricted airspace (Class D)"
            ],
            "classification": "UNKNOWN",
            "escalate": True
        }
