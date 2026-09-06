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

# --- НОВЫЙ ИМПОРТ ДЛЯ v0.3 ---
from core.semantic_analyzer import SemanticAnalyzer


class EventNormalizer:
    """
    Event Normalizer extracts critical conditions from incident descriptions.
    Now with Semantic Integrity (v0.3).
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
        # --- НОВЫЙ КОМПОНЕНТ v0.3 ---
        self.semantic_analyzer = SemanticAnalyzer()

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

        # --- ОБНОВЛЁННОЕ ИЗВЛЕЧЕНИЕ С СЕМАНТИКОЙ ---
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
            # --- НОВЫЕ ПОЛЯ ДЛЯ СЕМАНТИКИ ---
            "semantic_summary": semantic_summary,
            "status": "NORMALIZED"
        }

        self.critical_conditions = critical_conditions
        return {**input_data, **normalized_data}

    # --- ОБНОВЛЁННЫЙ МЕТОД С СЕМАНТИЧЕСКИМ АНАЛИЗОМ ---
    def _extract_critical_conditions(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract critical conditions with semantic analysis.
        
        Handles:
        - Polarity (positive, negative, neutral)
        - Negation (no, not, without, never)
        - Uncertainty (possible, suspected, maybe)
        - Context (previous, historical, reported)
        """
        conditions = []
        text_lower = text.lower()

        for condition_type, config in self.CRITICAL_KEYWORDS.items():
            for keyword in config["keywords"]:
                if keyword in text_lower:
                    # --- СЕМАНТИЧЕСКИЙ АНАЛИЗ ---
                    analysis = self.semantic_analyzer.analyze(text, keyword)

                    # Если ключевое слово найдено, но отрицается — пропускаем
                    if analysis["detected"] and analysis["polarity"] == "NEGATIVE":
                        continue

                    # Определяем severity на основе семантики
                    severity = config["severity"]
                    if analysis["uncertainty"] == "HIGH":
                        if severity == "CRITICAL":
                            severity = "HIGH"
                        elif severity == "HIGH":
                            severity = "MEDIUM"

                    # Пропускаем исторический контекст
                    if analysis["context"] == "PREVIOUS":
                        continue

                    # Находим контекстное окружение
                    position = text_lower.find(keyword)
                    start = max(0, position - 30)
                    end = min(len(text), position + 50)
                    context = text[start:end].strip()

                    conditions.append({
                        "condition": condition_type.upper(),
                        "severity": severity,
                        "keyword": keyword,
                        "context": context,
                        # --- СЕМАНТИЧЕСКИЕ МЕТАДАННЫЕ ---
                        "polarity": analysis["polarity"],
                        "confidence": analysis["confidence"],
                        "uncertainty": analysis["uncertainty"],
                        "negation_found": analysis["negation_found"],
                        "uncertainty_found": analysis["uncertainty_found"],
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "source": "INCIDENT_INPUT",
                        "status": "ACTIVE"
                    })
                    break

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

        # Приоритет по severity
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
