"""
AVCS VIRTUAL COMPANY
Event Normalizer

EXTRACT critical conditions from raw incident description
PRESERVE all critical information
PASS structured conditions to Dispatcher
"""

from typing import Dict, Any, List
from datetime import datetime
import re


class EventNormalizer:
    """
    Event Normalizer extracts critical conditions from incident descriptions.
    """

    CRITICAL_KEYWORDS = {
        "fire": {"severity": "CRITICAL", "keywords": ["fire", "flame", "burning", "ignition"]},
        "smoke": {"severity": "HIGH", "keywords": ["smoke", "fume"]},
        "evacuation": {"severity": "CRITICAL", "keywords": ["evacuate", "evacuating", "abandon"]},
        "temperature": {"severity": "HIGH", "keywords": ["temperature", "heat", "overheat"]},
        "oil_spill": {"severity": "CRITICAL", "keywords": ["oil", "spill", "leak", "pollution", "environmental"]},
        "hull_breach": {"severity": "CRITICAL", "keywords": ["breach", "hull", "flood", "water ingress"]},
        "man_overboard": {"severity": "CRITICAL", "keywords": ["overboard", "man overboard", "MOB"]},
        "gas_leak": {"severity": "CRITICAL", "keywords": ["gas leak", "methane", "toxic"]},
        "drone": {"severity": "HIGH", "keywords": ["drone", "uav", "unidentified"]},
        "collision": {"severity": "CRITICAL", "keywords": ["collision", "impact", "strike"]},
        "explosion": {"severity": "CRITICAL", "keywords": ["explosion", "blast", "boom"]},
    }

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.critical_conditions = []

    def normalize(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw incident data."""
        description = input_data.get("description", "")
        object_type = input_data.get("object", "Unknown")
        position = input_data.get("position", "Unknown")

        critical_conditions = self._extract_critical_conditions(description)
        event_type = self._determine_event_type(critical_conditions)
        severity = self._determine_overall_severity(critical_conditions)
        is_emergency = severity in ["CRITICAL", "HIGH"]

        normalized_data = {
            "event_id": input_data.get("event_id", f"EVT-{datetime.utcnow().strftime('%Y%m%d')}-001"),
            "raw_description": description,
            "object": object_type,
            "position": position,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": event_type,
            "severity": severity,
            "is_emergency": is_emergency,
            "critical_conditions": critical_conditions,
            "critical_conditions_count": len(critical_conditions),
            "has_critical": any(c.get("severity") == "CRITICAL" for c in critical_conditions),
            "has_high": any(c.get("severity") == "HIGH" for c in critical_conditions),
            "status": "NORMALIZED"
        }

        self.critical_conditions = critical_conditions
        return {**input_data, **normalized_data}

    def _extract_critical_conditions(self, text: str) -> List[Dict[str, Any]]:
        """Extract critical conditions from text."""
        conditions = []
        text_lower = text.lower()

        for condition_type, config in self.CRITICAL_KEYWORDS.items():
            for keyword in config["keywords"]:
                if keyword in text_lower:
                    position = text_lower.find(keyword)
                    start = max(0, position - 30)
                    end = min(len(text), position + 50)
                    context = text[start:end].strip()

                    conditions.append({
                        "condition": condition_type.upper(),
                        "severity": config["severity"],
                        "keyword": keyword,
                        "context": context,
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "source": "INCIDENT_INPUT",
                        "status": "ACTIVE"
                    })
                    break

        return conditions

    def _determine_event_type(self, conditions: List[Dict[str, Any]]) -> str:
        """Determine event type based on conditions."""
        if not conditions:
            return "GENERAL"

        for condition in conditions:
            if condition["severity"] == "CRITICAL":
                return condition["condition"]

        for condition in conditions:
            if condition["severity"] == "HIGH":
                return condition["condition"]

        return conditions[0]["condition"]

    def _determine_overall_severity(self, conditions: List[Dict[str, Any]]) -> str:
        """Determine overall severity based on critical conditions."""
        if any(c.get("severity") == "CRITICAL" for c in conditions):
            return "CRITICAL"
        if any(c.get("severity") == "HIGH" for c in conditions):
            return "HIGH"
        return "LOW"

    def get_critical_conditions(self) -> List[Dict[str, Any]]:
        """Return critical conditions."""
        return self.critical_conditions
