"""
AVCS VIRTUAL COMPANY
Risk Engine

Determines risk based on critical conditions.
"""

from typing import Dict, Any, List


class RiskEngine:
    """
    Risk Engine determines risk level based on critical conditions.
    
    Responsibilities:
    - Evaluate critical conditions
    - Determine overall risk
    - Identify specific risks
    - Provide risk justification
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def evaluate_risk(self, critical_conditions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate risk based on critical conditions.
        
        Args:
            critical_conditions: List of critical conditions
            
        Returns:
            Risk assessment
        """
        risks = []
        overall_risk = "LOW"

        for condition in critical_conditions:
            severity = condition.get("severity", "LOW")
            condition_type = condition.get("condition", "UNKNOWN")

            if severity == "CRITICAL":
                overall_risk = "CRITICAL"
                risks.append({
                    "condition": condition_type,
                    "severity": "CRITICAL",
                    "description": f"{condition_type} detected — immediate action required"
                })
            elif severity == "HIGH" and overall_risk != "CRITICAL":
                overall_risk = "HIGH"
                risks.append({
                    "condition": condition_type,
                    "severity": "HIGH",
                    "description": f"{condition_type} detected — prompt attention required"
                })
            else:
                risks.append({
                    "condition": condition_type,
                    "severity": "LOW",
                    "description": f"{condition_type} detected — monitor"
                })

        return {
            "overall_risk": overall_risk,
            "risks": risks,
            "risk_count": len(risks),
            "has_critical_risk": any(r["severity"] == "CRITICAL" for r in risks),
            "status": "COMPLETED"
        }

    def get_risk_for_decision(self, critical_conditions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get risk assessment for Decision Engine.
        
        Args:
            critical_conditions: List of critical conditions
            
        Returns:
            Risk assessment for decision
        """
        risk_result = self.evaluate_risk(critical_conditions)

        # Map risk to action constraints
        if risk_result["overall_risk"] == "CRITICAL":
            risk_result["action_constraints"] = {
                "recommend_continue": False,
                "recommend_intervention": True,
                "requires_immediate_action": True,
                "default_action": "STOP_INTERVENTION"
            }
        elif risk_result["overall_risk"] == "HIGH":
            risk_result["action_constraints"] = {
                "recommend_continue": False,
                "recommend_intervention": True,
                "requires_immediate_action": False,
                "default_action": "CHANGE_COURSE"
            }
        else:
            risk_result["action_constraints"] = {
                "recommend_continue": True,
                "recommend_intervention": False,
                "requires_immediate_action": False,
                "default_action": "CONTINUE"
            }

        return risk_result
