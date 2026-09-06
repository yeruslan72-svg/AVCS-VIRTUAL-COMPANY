"""
AVCS VIRTUAL COMPANY
Event Normalizer

EXTRACT critical conditions from raw incident description
PRESERVE all critical information
PASS structured conditions to Dispatcher

Version: v0.3.4 — Fixed confirmation detection
"""

from typing import Dict, Any, List
from datetime import datetime
import re


class EventNormalizer:
    """
    Event Normalizer extracts critical conditions from incident descriptions.
    Now with built-in semantic detection (negation, uncertainty, confirmation).
    """

    CRITICAL_KEYWORDS = {
        "fire": {"severity": "CRITICAL", "keywords": ["fire", "flame", "burning", "ignition"]},
        "smoke": {"severity": "HIGH", "keywords": ["smoke", "fume"]},
        "evacuation": {"severity": "CRITICAL", "keywords": ["evacuate", "evacuating", "abandon"]},
        "temperature": {"severity": "HIGH", "keywords": ["temperature", "heat", "overheat"]},
        "oil_spill": {"severity": "CRITICAL", "keywords": ["oil", "spill", "leak", "pollution", "environmental"]},
        "hull_breach": {"severity": "CRITICAL", "keywords": ["water ingress", "breach", "hull", "flood"]},
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
        """
        Normalize raw incident data with semantic analysis.
        
        Args:
            input_data: Raw incident data with description
            
        Returns:
            Normalized data with critical conditions and semantic metadata
        """
        description = input_data.get("description", "")
        object_type = input_data.get("object", "Unknown")
        position = input_data.get("position", "Unknown")

        # Извлечение critical conditions с семантикой
        critical_conditions = self._extract_critical_conditions(description)

        # Определяем event type и severity
        event_type = self._determine_event_type(critical_conditions)
        severity = self._determine_overall_severity(critical_conditions)
        is_emergency = severity in ["CRITICAL", "HIGH"]

        # Собираем семантическую информацию
        semantic_summary = self._build_semantic_summary(critical_conditions)

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
            "semantic_summary": semantic_summary,
            "status": "NORMALIZED"
        }

        self.critical_conditions = critical_conditions
        return {**input_data, **normalized_data}

    def _extract_critical_conditions(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract critical conditions with built-in semantic detection.
        
        Handles:
        - Confirmation (detected, confirmed, verified)
        - Negation (no, not, without, never, ruled out)
        - Uncertainty (suspected, possible, probable, appears, seems)
        - Context (previous, historical, reported)
        """
        conditions = []
        text_lower = text.lower()

        # Паттерны для семантического анализа
        negation_patterns = [
            r"\bno\s+", r"\bnot\s+", r"\bwithout\s+",
            r"\bnever\s+", r"\bruled\s+out\s*", r"\bexcluded\s*",
            r"\babsent\s*", r"\bnot\s+detected\s*", r"\bno\s+evidence\s*"
        ]

        confirmation_patterns = [
            r"\bdetected\s+", r"\bconfirmed\s+", r"\bverified\s+", r"\bvalidated\s+"
        ]

        uncertainty_patterns = [
            r"\bsuspected\s+", r"\bpossible\s+", r"\bprobable\s+",
            r"\bprobably\s+", r"\bmaybe\s+", r"\bpotential\s+",
            r"\bappears?\s*", r"\bseems?\s*", r"\bindicates?\s*",
            r"\bsuggests?\s*"
        ]

        context_patterns = {
            "previous": [r"\bprevious\s+", r"\bprior\s+", r"\bhistorical\s+", r"\bearlier\s+"],
            "reported": [r"\breported\s+", r"\bstated\s+", r"\baccording to\s+"],
            "confirmed": [r"\bconfirmed\s+", r"\bverified\s+", r"\bvalidated\s+"],
        }

        for condition_type, config in self.CRITICAL_KEYWORDS.items():
            for keyword in config["keywords"]:
                if keyword not in text_lower:
                    continue

                position = text_lower.find(keyword)

                # --- СЕМАНТИЧЕСКОЕ ОКНО ---
                window_start = max(0, position - 50)
                window_end = min(len(text), position + len(keyword) + 50)
                window_text = text[window_start:window_end].lower()

                # --- ПРОВЕРКА ОТРИЦАНИЯ ---
                negation_found = False
                for pattern in negation_patterns:
                    if re.search(pattern, window_text):
                        negation_found = True
                        break

                if negation_found:
                    continue  # Пропускаем это условие

                # --- ПРОВЕРКА КОНТЕКСТА ---
                context_type = None
                for ctx_type, patterns in context_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, window_text):
                            context_type = ctx_type.upper()
                            break
                    if context_type:
                        break

                # Пропускаем исторический контекст
                if context_type == "PREVIOUS":
                    continue

                # --- ПРОВЕРКА ПОДТВЕРЖДЕНИЯ ---
                confirmation_found = False
                for pattern in confirmation_patterns:
                    if re.search(pattern, window_text):
                        confirmation_found = True
                        break

                if confirmation_found:
                    # Подтверждённое условие — добавляем
                    polarity = "POSITIVE"
                    uncertainty = None
                    confidence = 0.8
                    severity = config["severity"]
                else:
                    # --- ПРОВЕРКА НЕОПРЕДЕЛЁННОСТИ ---
                    uncertainty_found = False
                    for pattern in uncertainty_patterns:
                        if re.search(pattern, window_text):
                            uncertainty_found = True
                            break

                    if uncertainty_found:
                        # Неопределённость — пропускаем
                        continue
                    else:
                        # Обычное упоминание — добавляем
                        polarity = "POSITIVE"
                        uncertainty = None
                        confidence = 0.8
                        severity = config["severity"]

                # Контекст
                start = max(0, position - 30)
                end = min(len(text), position + 50)
                context = text[start:end].strip()

                conditions.append({
                    "condition": condition_type.upper(),
                    "severity": severity,
                    "keyword": keyword,
                    "context": context,
                    "polarity": polarity,
                    "confidence": confidence,
                    "uncertainty": uncertainty,
                    "negation_found": False,
                    "uncertainty_found": uncertainty_found if not confirmation_found else False,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "source": "INCIDENT_INPUT",
                    "status": "ACTIVE"
                })
                break  # Только одно условие на тип

        return conditions

    def _build_semantic_summary(self, conditions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build a summary of semantic information from all conditions."""
        if not conditions:
            return {
                "total_conditions": 0,
                "polarities": {},
                "uncertainties": [],
                "average_confidence": 0.0
            }

        polarities = {}
        uncertainties = []
        total_confidence = 0.0

        for cond in conditions:
            polarity = cond.get("polarity", "UNKNOWN")
            polarities[polarity] = polarities.get(polarity, 0) + 1

            if cond.get("uncertainty"):
                uncertainties.append(cond.get("uncertainty"))

            total_confidence += cond.get("confidence", 0.8)

        avg_confidence = total_confidence / len(conditions)

        return {
            "total_conditions": len(conditions),
            "polarities": polarities,
            "uncertainties": uncertainties,
            "average_confidence": avg_confidence,
            "has_negation": polarities.get("NEGATIVE", 0) > 0,
            "has_uncertainty": len(uncertainties) > 0
        }

    def _determine_event_type(self, conditions: List[Dict[str, Any]]) -> str:
        """Determine event type based on conditions."""
        if not conditions:
            return "GENERAL"

        for condition in conditions:
            if condition.get("severity") == "CRITICAL":
                return condition["condition"]

        for condition in conditions:
            if condition.get("severity") == "HIGH":
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
