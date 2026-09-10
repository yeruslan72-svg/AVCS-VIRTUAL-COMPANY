"""
AVCS VIRTUAL COMPANY
GYRO Dpt. — Stability Under Pressure

CONTRACT:
PURPOSE: Assess whether the decision environment is stable enough for legitimate action.
AUTHORITY: Stability Assessment Authority.
PROHIBITED: Recommend actions, authorize maneuvers, execute, issue commands.
"""

from typing import Dict, Any, List
from datetime import datetime, timezone
from core.departments.base import BaseDepartment


class GyroDepartment(BaseDepartment):
    """
    GYRO Dpt. — Stability Under Pressure.

    GYRO does not analyze motion.
    GYRO does not calculate trajectories.
    GYRO does not recommend actions.

    GYRO assesses whether the decision environment is stable enough
    for legitimate action.

    A gyroscope does not accelerate movement.
    It prevents loss of balance.
    """

    STABILITY_STATES = {
        "STABLE": "environment supports legitimate action",
        "CONDITIONALLY_STABLE": "environment supports action with constraints",
        "UNSTABLE": "environment does not support legitimate action",
        "UNDETERMINED": "stability cannot be assessed",
    }

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("GYRO Dpt.", config)
        self.authority_state = "STABILITY_ASSESSMENT_AUTHORITY"

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess whether the decision environment is stable enough for action.

        Required input fields:
        - human_condition: cognitive/physical state of operators
        - system_condition: operational state of the system
        - load_level: current operational load (LOW / MEDIUM / HIGH)
        - environmental_conditions: external conditions (optional)

        Returns:
        - stability_status: STABLE / CONDITIONALLY STABLE / UNSTABLE / UNDETERMINED
        - load_level: HIGH / MEDIUM / LOW
        - human_condition: assessment
        - system_condition: assessment
        - risk_factors: identified stability risks
        - recommendation: MONITOR / ADJUST / HOLD / ESCALATE
        """

        human_condition = input_data.get("human_condition")
        system_condition = input_data.get("system_condition")
        load_level = input_data.get("load_level", "MEDIUM")
        environmental_conditions = input_data.get("environmental_conditions", {})

        self.event_id = input_data.get("event_id") or self._generate_event_id()

        self._log(
            f"GYRO stability assessment — load={load_level}, "
            f"human={human_condition}, system={system_condition}"
        )

        if not human_condition and not system_condition:
            return self._create_response(
                assessment="UNDETERMINED — no stability data provided",
                evidence=[],
                confidence=0.0,
                uncertainty=["human_condition and system_condition are required"],
                status="UNDETERMINED",
                stability_status="UNDETERMINED",
                load_level=load_level,
                authority_state=self.authority_state,
                event_id=self.event_id,
            )

        # -------------------------------------------------------------------
        # Stability assessment — structural, not interpretive
        # -------------------------------------------------------------------

        evidence: List[str] = []
        risk_factors: List[str] = []
        uncertainty: List[str] = []

        # Human condition
        if human_condition == "FATIGUED":
            risk_factors.append("Human fatigue detected")
            evidence.append("Human condition: FATIGUED")
        elif human_condition == "OVERLOADED":
            risk_factors.append("Human cognitive overload detected")
            evidence.append("Human condition: OVERLOADED")
        elif human_condition == "READY":
            evidence.append("Human condition: READY")
        else:
            uncertainty.append("Human condition: UNKNOWN")

        # System condition
        if system_condition == "DEGRADED":
            risk_factors.append("System degraded")
            evidence.append("System condition: DEGRADED")
        elif system_condition == "UNSTABLE":
            risk_factors.append("System unstable")
            evidence.append("System condition: UNSTABLE")
        elif system_condition == "NOMINAL":
            evidence.append("System condition: NOMINAL")
        else:
            uncertainty.append("System condition: UNKNOWN")

        # Load level
        if load_level == "HIGH":
            risk_factors.append("Operational load HIGH")
            evidence.append("Load level: HIGH")
        elif load_level == "MEDIUM":
            evidence.append("Load level: MEDIUM")
        elif load_level == "LOW":
            evidence.append("Load level: LOW")
        else:
            uncertainty.append("Load level: UNKNOWN")

        # Environmental conditions
        if environmental_conditions.get("hostile"):
            risk_factors.append("Hostile environmental conditions")
        if environmental_conditions.get("deteriorating"):
            risk_factors.append("Deteriorating environmental conditions")

        # -------------------------------------------------------------------
        # Determine stability status — structural, not interpretive
        # -------------------------------------------------------------------

        if uncertainty and not risk_factors:
            stability_status = "UNDETERMINED"
            recommendation = "ESCALATE"
            assessment = (
                "UNDETERMINED — stability cannot be confirmed: "
                + ", ".join(uncertainty)
            )
        elif len(risk_factors) >= 3:
            stability_status = "UNSTABLE"
            recommendation = "HOLD"
            assessment = (
                "UNSTABLE — environment does not support legitimate action: "
                + ", ".join(risk_factors)
            )
        elif risk_factors:
            stability_status = "CONDITIONALLY STABLE"
            recommendation = "ADJUST"
            assessment = (
                "CONDITIONALLY STABLE — action possible with constraints: "
                + ", ".join(risk_factors)
            )
        else:
            stability_status = "STABLE"
            recommendation = "MONITOR"
            assessment = "STABLE — environment supports legitimate action"

        # -------------------------------------------------------------------
        # Response
        # -------------------------------------------------------------------

        return self._create_response(
            assessment=assessment,
            evidence=evidence,
            confidence=0.90 if stability_status == "STABLE"
                       else 0.85 if stability_status == "UNSTABLE"
                       else 0.70 if stability_status == "CONDITIONALLY STABLE"
                       else 0.60,
            uncertainty=uncertainty,
            constraints=risk_factors,
            recommendations=[recommendation],  # GYRO recommends only stability action
            status="COMPLETED",
            event_id=self.event_id,
            stability_status=stability_status,
            load_level=load_level,
            human_condition=human_condition,
            system_condition=system_condition,
            risk_factors=risk_factors,
            authority_state=self.authority_state,
        )

    def get_contract(self) -> Dict[str, Any]:
        """Return the GYRO Dpt. contract — Stability Under Pressure."""
        return {
            "department": self.department_name,
            "purpose": "Assess whether the decision environment is stable enough for legitimate action.",
            "authority": "STABILITY_ASSESSMENT_AUTHORITY",
            "question": "Is the environment stable enough to act?",
            "stability_states": self.STABILITY_STATES,
            "permitted_outputs": [
                "STABLE",
                "CONDITIONALLY STABLE",
                "UNSTABLE",
                "UNDETERMINED — ESCALATION REQUIRED",
            ],
            "permitted_recommendations": [
                "MONITOR",
                "ADJUST",
                "HOLD",
                "ESCALATE",
            ],
            "prohibited_decisions": [
                "recommend operational actions",
                "authorize maneuvers",
                "issue commands",
                "execute",
                "determine final threat",
            ],
        }
