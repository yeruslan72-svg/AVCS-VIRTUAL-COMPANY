"""
AVCS VIRTUAL COMPANY
HELM Dpt. — Decision Authority

CONTRACT:
PURPOSE: Make legitimate, bounded, and structurally supported decisions under pressure.
AUTHORITY: DECISION_AUTHORITY (within North).
PROHIBITED: Execute, issue commands, authorize own decision, bypass COMPASS or CAPTAIN.
"""

from typing import Dict, Any, List
from datetime import datetime, timezone
from core.departments.base import BaseDepartment


class HelmDepartment(BaseDepartment):
    """
    HELM Dpt. — Decision Authority.

    HELM does not execute.
    HELM does not issue commands.
    HELM does not authorize its own decision.

    HELM receives inputs from all departments and makes a decision
    within the boundaries defined by North.

    The helm is always held by the person who carries the consequence.
    """

    DECISION_STATES = {
        "DECISION_MADE": "a legitimate decision has been made within North",
        "NO_DECISION": "no decision could be made within North",
        "DEFERRED": "decision deferred pending additional input",
        "ESCALATED": "decision requires CAPTAIN review",
    }

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("HELM Dpt.", config)
        self.authority_state = "DECISION_AUTHORITY"

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a decision based on inputs from all departments.

        Required input fields:
        - assessments: dict of department assessments (from Aggregator)
        - north_status: WITHIN NORTH / OUTSIDE NORTH / UNDETERMINED (from COMPASS)
        - stability_status: STABLE / CONDITIONALLY STABLE / UNSTABLE (from GYRO)
        - reality_status: STRUCTURED / CONTRADICTORY / UNDETERMINED (from CHARTS)
        - conflict_result: result of conflict detection (optional)

        Returns:
        - decision: the decision made within North
        - decision_state: DECISION_MADE / NO_DECISION / DEFERRED / ESCALATED
        - basis: evidence supporting the decision
        - authority: DECISION_AUTHORITY
        """

        assessments = input_data.get("assessments", {})
        north_status = input_data.get("north_status")
        stability_status = input_data.get("stability_status")
        reality_status = input_data.get("reality_status")
        conflict_result = input_data.get("conflict_result", {})

        self.event_id = input_data.get("event_id") or self._generate_event_id()

        self._log(
            f"HELM decision process — north={north_status}, "
            f"stability={stability_status}, reality={reality_status}"
        )

        # -------------------------------------------------------------------
        # Decision boundary check — North
        # -------------------------------------------------------------------

        evidence: List[str] = []
        uncertainty: List[str] = []
        constraints: List[str] = []

        # North check (from COMPASS)
        if north_status == "OUTSIDE NORTH":
            return self._create_response(
                assessment="NO_DECISION — North violation",
                evidence=["COMPASS: OUTSIDE NORTH"],
                confidence=0.95,
                uncertainty=[],
                constraints=["North violation"],
                recommendations=["ESCALATE to CAPTAIN"],
                status="NO_DECISION",
                event_id=self.event_id,
                decision=None,
                decision_state="NO_DECISION",
                authority_state=self.authority_state,
            )
        elif north_status == "UNDETERMINED":
            uncertainty.append("North status: UNDETERMINED")
            constraints.append("North not confirmed")
        elif north_status == "WITHIN NORTH":
            evidence.append("COMPASS: WITHIN NORTH")

        # Stability check (from GYRO)
        if stability_status == "UNSTABLE":
            uncertainty.append("Stability: UNSTABLE")
            constraints.append("Environment not stable for action")
        elif stability_status == "CONDITIONALLY STABLE":
            evidence.append("GYRO: CONDITIONALLY STABLE")
            constraints.append("Action possible with constraints")
        elif stability_status == "STABLE":
            evidence.append("GYRO: STABLE")

        # Reality check (from CHARTS)
        if reality_status == "CONTRADICTORY":
            uncertainty.append("Reality: CONTRADICTORY")
            constraints.append("Conflicting evidence")
        elif reality_status == "UNDETERMINED":
            uncertainty.append("Reality: UNDETERMINED")
        elif reality_status == "STRUCTURED":
            evidence.append("CHARTS: STRUCTURED")

        # -------------------------------------------------------------------
        # Determine decision state — structural, not interpretive
        # -------------------------------------------------------------------

        # If North is not confirmed, defer or escalate
        if north_status == "UNDETERMINED":
            decision_state = "ESCALATED"
            decision = None
            assessment = (
                "ESCALATED — North not confirmed; decision requires CAPTAIN review"
            )
        # If stability is unstable, defer
        elif stability_status == "UNSTABLE":
            decision_state = "DEFERRED"
            decision = None
            assessment = (
                "DEFERRED — environment not stable for action"
            )
        # If reality is contradictory, defer
        elif reality_status == "CONTRADICTORY":
            decision_state = "DEFERRED"
            decision = None
            assessment = (
                "DEFERRED — conflicting evidence; reality not established"
            )
        # If there are conflicts, escalate
        elif conflict_result.get("has_conflicts"):
            decision_state = "ESCALATED"
            decision = None
            assessment = (
                "ESCALATED — conflicts detected; requires CAPTAIN review"
            )
        # Otherwise, make a decision
        else:
            decision_state = "DECISION_MADE"

            # Decision logic — minimal structural placeholder
            # In full AVCS, this is where the decision is formulated
            if north_status == "WITHIN NORTH" and stability_status in ("STABLE", "CONDITIONALLY STABLE"):
                decision = {
                    "type": "CONTINUE_WITH_CONSTRAINTS"
                    if constraints else "CONTINUE",
                    "constraints": constraints,
                    "basis": evidence,
                }
                assessment = (
                    f"DECISION MADE — {decision['type']} "
                    f"({len(constraints)} constraints)"
                )
            else:
                decision_state = "DEFERRED"
                decision = None
                assessment = (
                    "DEFERRED — insufficient structural support for decision"
                )

        # -------------------------------------------------------------------
        # Response
        # -------------------------------------------------------------------

        return self._create_response(
            assessment=assessment,
            evidence=evidence,
            confidence=0.90 if decision_state == "DECISION_MADE"
                       else 0.80 if decision_state == "ESCALATED"
                       else 0.70,
            uncertainty=uncertainty,
            constraints=constraints,
            recommendations=[],
            status=decision_state,
            event_id=self.event_id,
            decision=decision,
            decision_state=decision_state,
            basis=evidence,
            authority_state=self.authority_state,
        )

    def get_contract(self) -> Dict[str, Any]:
        """Return the HELM Dpt. contract — Decision Authority."""
        return {
            "department": self.department_name,
            "purpose": "Make legitimate, bounded, and structurally supported decisions under pressure.",
            "authority": "DECISION_AUTHORITY (within North)",
            "question": "What decision should be made?",
            "decision_states": self.DECISION_STATES,
            "permitted_outputs": [
                "DECISION_MADE",
                "NO_DECISION",
                "DEFERRED",
                "ESCALATED",
            ],
            "prohibited_decisions": [
                "execute",
                "issue commands",
                "authorize own decision",
                "bypass COMPASS",
                "bypass CAPTAIN",
                "violate North",
            ],
        }
