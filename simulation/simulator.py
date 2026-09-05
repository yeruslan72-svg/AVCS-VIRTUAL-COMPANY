"""
AVCS VIRTUAL COMPANY
Simulator — Event Simulation

FUNCTION:
- Simulate incoming events
- Test decision cycle
- Generate test data
"""

from typing import Dict, Any, Optional
from datetime import datetime
import random


class Simulator:
    """
    Simulator for testing AVCS decision cycle.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.events = []

    def generate_drone_event(self, scenario: str = "standard") -> Dict[str, Any]:
        """
        Generate a drone detection event.
        
        Args:
            scenario: "standard", "close", "hostile"
            
        Returns:
            Event data
        """
        base_event = {
            "event_id": f"SIM-{datetime.utcnow().strftime('%Y%m%d')}-{random.randint(100, 999)}",
            "object": "Unidentified Drone",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "observations": []
        }

        if scenario == "standard":
            event = {
                **base_event,
                "position": f"{random.uniform(0.5, 2.0):.1f} NM, Bearing {random.randint(180, 360)}°",
                "heading": random.randint(0, 360),
                "speed": random.randint(10, 40),
                "altitude": random.randint(100, 500),
                "threat_heading": random.randint(0, 360),
                "threat_speed": random.randint(10, 40),
                "separation_required": random.uniform(0.5, 1.0),
                "classification": "UNKNOWN",
                "escalate": True
            }
        elif scenario == "close":
            event = {
                **base_event,
                "position": f"{random.uniform(0.1, 0.5):.1f} NM, Bearing {random.randint(180, 360)}°",
                "heading": random.randint(0, 360),
                "speed": random.randint(30, 60),
                "altitude": random.randint(50, 200),
                "threat_heading": random.randint(0, 360),
                "threat_speed": random.randint(30, 60),
                "separation_required": random.uniform(0.1, 0.3),
                "classification": "UNKNOWN",
                "escalate": True
            }
        elif scenario == "hostile":
            event = {
                **base_event,
                "position": f"{random.uniform(0.1, 0.3):.1f} NM, Bearing {random.randint(180, 360)}°",
                "heading": random.randint(0, 360),
                "speed": random.randint(50, 80),
                "altitude": random.randint(20, 100),
                "threat_heading": random.randint(0, 360),
                "threat_speed": random.randint(50, 80),
                "separation_required": random.uniform(0.05, 0.15),
                "classification": "HOSTILE",
                "escalate": True
            }
        else:
            event = base_event

        self.events.append(event)
        return event

    def get_events(self) -> list:
        """Get all generated events."""
        return self.events

    def clear_events(self):
        """Clear all events."""
        self.events = []
