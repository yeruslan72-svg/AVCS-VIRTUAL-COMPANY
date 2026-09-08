"""
AVCS VIRTUAL COMPANY
Streamlit UI — Operational Decision Dashboard
Version: v0.3.7 — Embedded Semantic Event Normalizer
"""

import sys
import os
import streamlit as st
import json
from datetime import datetime
import re

# Добавляем корневую папку проекта в sys.path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# Импорт департаментов и других компонентов
from core.departments import (
    LookoutDepartment,
    ChartsDepartment,
    GyroDepartment,
    NavigatorDepartment,
    CompassDepartment,
    HelmDepartment,
    CaptainDepartment,
)
from core.dispatcher import Dispatcher
from core.aggregation import Aggregator
from core.conflict_detection import ConflictDetector
from core.decision_engine import DecisionEngine
from core.authority_gate import AuthorityGate
from core.state_machine import StateMachine
from core.risk_engine import RiskEngine
from records.incident_registry import IncidentRegistry


# =============================================================================
# ВСТРОЕННЫЙ SEMANTIC EVENT NORMALIZER v0.3.7
# =============================================================================

class SemanticEventNormalizer:
    """
    Встроенный нормализатор событий с полной семантикой:
    - Обнаружение ключевых слов
    - Отрицание (no, not, without, ruled out)
    - Неопределённость (suspected, possible, appears)
    - Временной контекст (previous, reported, current)
    - Единый контракт для critical_conditions
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

    NEGATION_PATTERNS = [
        r"\bno\s+", r"\bnot\s+", r"\bwithout\s+",
        r"\bnever\s+", r"\bruled\s+out\s*", r"\bexcluded\s*",
        r"\babsent\s*", r"\bnot\s+detected\s*", r"\bno\s+evidence\s*"
    ]

    UNCERTAINTY_PATTERNS = [
        r"\bsuspected\s+", r"\bpossible\s+", r"\bprobable\s+",
        r"\bprobably\s+", r"\bmaybe\s+", r"\bpotential\s+",
        r"\bappears?\s*", r"\bseems?\s*", r"\bindicates?\s*",
        r"\bsuggests?\s*"
    ]

    TEMPORAL_PATTERNS = {
        "previous": [r"\bprevious\s+", r"\bprior\s+", r"\bhistorical\s+", r"\bearlier\s+"],
        "reported": [r"\breported\s+", r"\bstated\s+", r"\baccording to\s+"],
        "current": [r"\bcurrent\s+", r"\bnow\s+", r"\bat this time\s+"],
        "confirmed": [r"\bconfirmed\s+", r"\bverified\s+", r"\bvalidated\s+"],
    }

    def normalize(self, text: str) -> dict:
        """
        Полная нормализация текста события.
        Возвращает:
        - critical_conditions: список условий
        - event_type: определённый тип события
        - severity: общий уровень серьёзности
        - semantic_summary: сводка по семантике
        """
        conditions = self._extract_critical_conditions(text)
        event_type = self._determine_event_type(conditions)
        severity = self._determine_overall_severity(conditions)
        semantic_summary = self._build_semantic_summary(conditions)

        return {
            "critical_conditions": conditions,
            "critical_conditions_count": len(conditions),
            "event_type": event_type,
            "severity": severity,
            "has_critical": any(c.get("severity") == "CRITICAL" for c in conditions),
            "has_high": any(c.get("severity") == "HIGH" for c in conditions),
            "semantic_summary": semantic_summary,
            "status": "NORMALIZED"
        }

    def _extract_critical_conditions(self, text: str) -> list:
        """Извлечение критических условий с полной семантикой."""
        conditions = []
        text_lower = text.lower()

        for condition_type, config in self.CRITICAL_KEYWORDS.items():
            for keyword in config["keywords"]:
                if keyword not in text_lower:
                    continue

                position = text_lower.find(keyword)

                # Semantic Window
                window_start = max(0, position - 50)
                window_end = min(len(text), position + len(keyword) + 50)
                window_text = text[window_start:window_end].lower()

                # --- ОТРИЦАНИЕ ---
                negation_found = False
                for pattern in self.NEGATION_PATTERNS:
                    if re.search(pattern, window_text):
                        negation_found = True
                        break

                if negation_found:
                    continue  # Пропускаем условие

                # --- ВРЕМЕННОЙ КОНТЕКСТ ---
                temporal_context = None
                for ctx_type, patterns in self.TEMPORAL_PATTERNS.items():
                    for pattern in patterns:
                        if re.search(pattern, window_text):
                            temporal_context = ctx_type.upper()
                            break
                    if temporal_context:
                        break

                if temporal_context == "PREVIOUS":
                    continue  # Пропускаем историческое упоминание

                # --- НЕОПРЕДЕЛЁННОСТЬ ---
                uncertainty_found = False
                for pattern in self.UNCERTAINTY_PATTERNS:
                    if re.search(pattern, window_text):
                        uncertainty_found = True
                        break

                # --- ОПРЕДЕЛЕНИЕ СТАТУСА ---
                if uncertainty_found:
                    polarity = "NEUTRAL"
                    uncertainty = "HIGH"
                    confidence = 0.6
                    severity = config["severity"]
                else:
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
                    "uncertainty_found": uncertainty_found,
                    "temporal_context": temporal_context,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "source": "INCIDENT_INPUT",
                    "status": "ACTIVE"
                })
                break

        return conditions

    def _determine_event_type(self, conditions: list) -> str:
        """Определение типа события."""
        if not conditions:
            return "GENERAL"
        for c in conditions:
            if c.get("severity") == "CRITICAL":
                return c["condition"]
        for c in conditions:
            if c.get("severity") == "HIGH":
                return c["condition"]
        return conditions[0]["condition"]

    def _determine_overall_severity(self, conditions: list) -> str:
        """Определение общего уровня серьёзности."""
        if any(c.get("severity") == "CRITICAL" for c in conditions):
            return "CRITICAL"
        if any(c.get("severity") == "HIGH" for c in conditions):
            return "HIGH"
        return "LOW"

    def _build_semantic_summary(self, conditions: list) -> dict:
        """Сводка по семантике."""
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

        return {
            "total_conditions": len(conditions),
            "polarities": polarities,
            "uncertainties": uncertainties,
            "average_confidence": total_confidence / len(conditions),
            "has_negation": polarities.get("NEGATIVE", 0) > 0,
            "has_uncertainty": len(uncertainties) > 0
        }


# --- Настройка страницы ---
st.set_page_config(
    page_title="AVCS Virtual Company",
    page_icon="🧭",
    layout="wide"
)

# ... (остальная часть кода остаётся без изменений, начиная с приветственной страницы и далее)
# Я продолжу в следующем сообщении, чтобы не превысить лимит.
