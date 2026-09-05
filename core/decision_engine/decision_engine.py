"""
AVCS VIRTUAL COMPANY
Decision Engine — Decision Proposal Generator

FUNCTION:
- Convert aggregated operational state into a structured Decision Proposal
- Use risk assessment to determine action
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class DecisionEngine:
    """
    Decision Engine converts aggregated state into Decision Proposal.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.decision_log = []

    def formulate(self, aggregated_state: Dict[str, Any], conflict_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formulate a Decision Proposal from aggregated state and conflict result.
        """
        event_id = aggregated_state.get("event_id", "UNKNOWN")
        self._log(f"Formulating decision proposal for event: {event_id}")

        # Получаем оценку риска
        risk_assessment = aggregated_state.get("risk_assessment", {})
        overall_risk = risk_assessment.get("overall_risk", "LOW")
        risks = risk_assessment.get("risks", [])

        # Извлекаем данные
        assessments = aggregated_state.get("assessments", {})
        evidence = aggregated_state.get("evidence", [])
        recommendations = aggregated_state.get("recommendations", [])
        uncertainty = aggregated_state.get("uncertainty", [])
        has_conflict = conflict_result.get("has_conflicts", False)
        decision_blocked = conflict_result.get("decision_blocked", False)
        conflicts = conflict_result.get("conflicts", [])

        # --- ОПРЕДЕЛЯЕМ ПРЕДЛАГАЕМОЕ ДЕЙСТВИЕ НА ОСНОВЕ РИСКА ---
        options = []
        proposed_action = None

        # Определяем основной вариант
        if overall_risk == "CRITICAL":
            proposed_action = {
                "action": "STOP_INTERVENTION",
                "description": "Immediate intervention required — critical risk detected",
                "risk": "CRITICAL"
            }
            options.append(proposed_action)
            options.append({
                "action": "CHANGE_COURSE",
                "description": "Adjust course to avoid critical area",
                "risk": "HIGH"
            })
            options.append({
                "action": "MONITOR",
                "description": "Continue monitoring with increased attention",
                "risk": "MEDIUM"
            })
        elif overall_risk == "HIGH":
            proposed_action = {
                "action": "CHANGE_COURSE",
                "description": "High risk detected — course adjustment recommended",
                "risk": "HIGH"
            }
            options.append(proposed_action)
            options.append({
                "action": "MONITOR",
                "description": "Continue monitoring with increased attention",
                "risk": "MEDIUM"
            })
            options.append({
                "action": "CONTINUE",
                "description": "Continue with caution",
                "risk": "LOW"
            })
        else:
            proposed_action = {
                "action": "CONTINUE",
                "description": "Continue observation",
                "risk": "LOW"
            }
            options.append(proposed_action)
            options.append({
                "action": "MONITOR",
                "description": "Continue standard monitoring",
                "risk": "LOW"
            })

        # Если решение заблокировано конфликтами
        if decision_blocked:
            proposed_action = {
                "action": "BLOCKED",
                "description": "Decision blocked due to conflicts",
                "risk": "HIGH"
            }
            options = [proposed_action]

        # Определяем authority requirement
        if overall_risk in ["CRITICAL", "HIGH"]:
            authority_required = "CAPTAIN Dpt. (Immediate)"
        else:
            authority_required = "CAPTAIN Dpt."

        # Формируем Decision Proposal
        decision_proposal = {
            "event_id": event_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "operational_state": {
                "assessments": assessments,
                "constraints": aggregated_state.get("constraints", []),
                "uncertainty": uncertainty
            },
            "evidence": evidence,
            "risks": risks,
            "recommendations": recommendations,
            "available_options": options,
            "constraints": aggregated_state.get("constraints", []),
            "conflicts": conflicts,
            "has_conflict": has_conflict,
            "decision_blocked": decision_blocked,
            "authority_required": authority_required,
            "proposed_action": proposed_action,
            "status": "PROPOSAL_READY",
            "risk_assessment": risk_assessment
        }

        self.decision_log.append(decision_proposal)
        return decision_proposal

    def _log(self, message: str, level: str = "INFO"):
        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[{timestamp}] [DECISION_ENGINE] [{level}] {message}")

    def get_decision_log(self) -> List[Dict[str, Any]]:
        return self.decision_log
