"""
AVCS VIRTUAL COMPANY
COMPASS Dpt. — North Integrity / Boundary Authority

CONTRACT:
PURPOSE: Determine whether a proposed decision remains within North.
AUTHORITY: Boundary Authority (veto on violation of North).
PROHIBITED: Recommend actions, calculate trajectories, issue commands, execute.
"""

from typing import Dict, Any, List
from datetime import datetime, timezone
from core.departments.base import BaseDepartment


class CompassDepartment(BaseDepartment):
    """
    COMPASS Dpt. — North Integrity.

    COMPASS does not recommend actions.
    COMPASS does not calculate trajectories.
    COMPASS does not execute.

    COMPASS determines whether a proposed decision remains within North.

    North is defined by the AVCS Constitution as:

    1. Structural Integrity — the system remains within established operational limits.
    2. Human Safety — people are not exposed to unacceptable risk.
    3. Operational Control — the system retains the ability to stop.

    North is:
    - Non-negotiable
    - Non-optimizable
    - Non-overrideable

    North is not interpreted.
    North is applied.
    """

    NORTH_CONDITIONS = {
        "STRUCTURAL_INTEGRITY": "system remains within established operational limits",
        "HUMAN_SAFETY": "people are not exposed to unacceptable risk",
        "OPERATIONAL_CONTROL": "system retains the ability to stop",
    }

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("COMPASS Dpt.", config)
        self.authority_state = "BOUNDARY_AUTHORITY"

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine whether the proposed decision remains within North.

        Required input fields:
        - decision_proposal: the proposed decision or action
        - operational_state: current operational state
        - risk_assessment: risk information (optional)

        Returns:
        - assessment: WITHIN NORTH / OUTSIDE NORTH / UNDETERMINED
        - authority_state: BOUNDARY_AUTHORITY
        - veto: True if OUTSIDE NORTH
        """

        decision_proposal = input_data.get("decision_proposal")
        operational_state = input_data.get("operational_state", {})
        risk_assessment = input_data.get("risk_assessment", {})

        self.event_id = input_data.get("event_id") or self._generate_event_id()

        self._log(
            f"COMPASS boundary check — decision: {decision_proposal}"
        )

        if not decision_proposal:
            return self._create_response(
                assessment="UNDETERMINED — no decision proposal provided",
                evidence=[],
                confidence=0.0,
                uncertainty=["decision_proposal is required for North check"],
                status="UNDETERMINED",
                north_status="UNDETERMINED",
                veto=False,
                authority_state=self.authority_state,
                event_id=self.event_id,
            )

        # -------------------------------------------------------------------
        # North check — structural, not interpretive
        # -------------------------------------------------------------------

        evidence: List[str] = []
        violations: List[str] = []
        uncertainty: List[str] = []

        # Condition 1 — Structural Integrity
        structural_integrity = operational_state.get("structural_integrity")
        if structural_integrity is False:
            violations.append("STRUCTURAL_INTEGRITY violated")
            evidence.append("Structural integrity: OUTSIDE limits")
        elif structural_integrity is True:
            evidence.append("Structural integrity: within limits")
        else:
            uncertainty.append("Structural integrity: UNKNOWN")

        # Condition 2 — Human Safety
        human_safety = operational_state.get("human_safety")
        if human_safety is False:
            violations.append("HUMAN_SAFETY violated")
            evidence.append("Human safety: unacceptable risk")
        elif human_safety is True:
            evidence.append("Human safety: acceptable")
        else:
            uncertainty.append("Human safety: UNKNOWN")

        # Condition 3 — Operational Control
        operational_control = operational_state.get("operational_control")
        if operational_control is False:
            violations.append("OPERATIONAL_CONTROL violated")
            evidence.append("Operational control: cannot stop")
        elif operational_control is True:
            evidence.append("Operational control: retained")
        else:
            uncertainty.append("Operational control: UNKNOWN")

        # -------------------------------------------------------------------
        # Determine North status — structural, not interpretive
        # -------------------------------------------------------------------

        if violations:
            north_status = "OUTSIDE NORTH"
            veto = True
            assessment = (
                "OUTSIDE NORTH — decision violates: "
                + ", ".join(violations)
            )
        elif uncertainty:
            north_status = "UNDETERMINED"
            veto = False
            assessment = (
                "UNDETERMINED — North compliance cannot be confirmed: "
                + ", ".join(uncertainty)
            )
        else:
            north_status = "WITHIN NORTH"
            veto = False
            assessment = "WITHIN NORTH — decision remains within all North conditions"

        # -------------------------------------------------------------------
        # Response
        # -------------------------------------------------------------------

        return self._create_response(
            assessment=assessment,
            evidence=evidence,
            confidence=0.95 if north_status == "OUTSIDE NORTH"
                       else 0.90 if north_status == "WITHIN NORTH"
                       else 0.60,
            uncertainty=uncertainty,
            constraints=violations,
            recommendations=[],  # COMPASS does not recommend actions
            status="COMPLETED",
            event_id=self.event_id,
            north_status=north_status,
            veto=veto,
            authority_state=self.authority_state,
        )

    def get_contract(self) -> Dict[str, Any]:
        """Return the COMPASS Dpt. contract — North Integrity."""
        return {
            "department": self.department_name,
            "purpose": "Determine whether a proposed decision remains within North.",
            "authority": "BOUNDARY_AUTHORITY (veto on violation of North)",
            "question": "Does this decision remain within North?",
            "north_conditions": self.NORTH_CONDITIONS,
            "permitted_outputs": [
                "WITHIN NORTH",
                "OUTSIDE NORTH",
                "UNDETERMINED — ESCALATION REQUIRED",
            ],
            "prohibited_decisions": [
                "recommend actions",
                "calculate trajectories",
                "issue commands",
                "execute",
                "interpret North",
                "adapt North to circumstances",
            ],
        }
