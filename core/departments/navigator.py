"""
AVCS VIRTUAL COMPANY
NAVIGATOR Dpt. — Strategy & Direction

CONTRACT:
PURPOSE: Define the course and anticipate change.
AUTHORITY: STRATEGIC_PROPOSAL_AUTHORITY.
PROHIBITED: Authorize action, execute, issue commands, assess final threat, override human authority.
"""

from typing import Dict, Any, List
from datetime import datetime, timezone
from core.departments.base import BaseDepartment


class NavigatorDepartment(BaseDepartment):
    """
    NAVIGATOR Dpt. — Strategy & Direction.

    NAVIGATOR does not authorize.
    NAVIGATOR does not execute.
    NAVIGATOR does not determine final threat.

    NAVIGATOR proposes a course.
    NAVIGATOR anticipates change.
    NAVIGATOR defines direction.

    A navigator proposes the course.
    The helm decides.
    """

    COURSE_STATES = {
        "PROPOSED": "a strategic course has been proposed",
        "MAINTAIN": "current course should be maintained",
        "ADJUST": "current course should be adjusted",
        "REORIENT": "strategic direction should be reoriented",
        "DEFERRED": "course proposal deferred pending additional input",
    }

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("NAVIGATOR Dpt.", config)
        self.authority_state = "STRATEGIC_PROPOSAL_AUTHORITY"

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Propose a strategic course and anticipate change.

        Required input fields:
        - current_state: current operational state (from other departments)
        - strategic_context: broader context for strategic direction (optional)
        - anticipated_changes: expected changes in the environment (optional)

        Returns:
        - course: proposed strategic direction
        - basis: evidence supporting the proposal
        - anticipated_changes: expected changes
        - risk_factors: strategic risks
        - course_state: PROPOSED / MAINTAIN / ADJUST / REORIENT / DEFERRED
        """

        current_state = input_data.get("current_state", {})
        strategic_context = input_data.get("strategic_context", {})
        anticipated_changes = input_data.get("anticipated_changes", [])

        self.event_id = input_data.get("event_id") or self._generate_event_id()

        self._log(
            f"NAVIGATOR strategic proposal — "
            f"context={bool(strategic_context)}, "
            f"changes={len(anticipated_changes)}"
        )

        # -------------------------------------------------------------------
        # Strategic proposal — direction, not threat
        # -------------------------------------------------------------------

        evidence: List[str] = []
        uncertainty: List[str] = []
        risk_factors: List[str] = []

        # Current state
        if current_state:
            evidence.append(
                f"Current state: {len(current_state)} inputs received"
            )
            for key, value in current_state.items():
                evidence.append(f"{key}: {value}")
        else:
            uncertainty.append("Current state not provided")

        # Strategic context
        if strategic_context:
            for key, value in strategic_context.items():
                evidence.append(f"Strategic context — {key}: {value}")
        else:
            uncertainty.append("Strategic context not provided")

        # Anticipated changes
        if anticipated_changes:
            for change in anticipated_changes:
                evidence.append(f"Anticipated change: {change}")
        else:
            uncertainty.append("No anticipated changes provided")

        # Risk factors
        for key, value in strategic_context.items():
            if "risk" in key.lower() or "threat" in key.lower():
                risk_factors.append(f"{key}: {value}")

        # -------------------------------------------------------------------
        # Determine course state — structural, not interpretive
        # -------------------------------------------------------------------

        if not current_state and not strategic_context:
            course_state = "DEFERRED"
            course = None
            assessment = (
                "DEFERRED — insufficient input for strategic proposal"
            )
        elif not anticipated_changes and not strategic_context:
            course_state = "MAINTAIN"
            course = {
                "direction": "MAINTAIN_CURRENT",
                "basis": evidence,
            }
            assessment = (
                "MAINTAIN — no strategic changes anticipated; "
                "maintain current course"
            )
        elif risk_factors:
            course_state = "ADJUST"
            course = {
                "direction": "ADJUST_COURSE",
                "basis": evidence,
                "risk_factors": risk_factors,
            }
            assessment = (
                f"ADJUST — {len(risk_factors)} strategic risk factors identified; "
                "course adjustment recommended"
            )
        else:
            course_state = "PROPOSED"
            course = {
                "direction": "PROPOSE_COURSE",
                "basis": evidence,
                "anticipated_changes": anticipated_changes,
            }
            assessment = (
                f"PROPOSED — strategic course proposed based on "
                f"{len(evidence)} inputs"
            )

        # -------------------------------------------------------------------
        # Response
        # -------------------------------------------------------------------

        return self._create_response(
            assessment=assessment,
            evidence=evidence,
            confidence=0.85 if course_state == "PROPOSED"
                       else 0.80 if course_state == "ADJUST"
                       else 0.75 if course_state == "MAINTAIN"
                       else 0.60,
            uncertainty=uncertainty,
            constraints=risk_factors,
            recommendations=[course_state],
            status="COMPLETED",
            event_id=self.event_id,
            course=course,
            course_state=course_state,
            anticipated_changes=anticipated_changes,
            risk_factors=risk_factors,
            authority_state=self.authority_state,
        )

    def get_contract(self) -> Dict[str, Any]:
        """Return the NAVIGATOR Dpt. contract — Strategy & Direction."""
        return {
            "department": self.department_name,
            "purpose": "Define the course and anticipate change.",
            "authority": "STRATEGIC_PROPOSAL_AUTHORITY",
            "question": "Where should we go?",
            "course_states": self.COURSE_STATES,
            "permitted_outputs": [
                "PROPOSED",
                "MAINTAIN",
                "ADJUST",
                "REORIENT",
                "DEFERRED",
            ],
            "permitted_recommendations": [
                "strategic direction",
                "course of action",
                "alternative courses",
                "anticipation of change",
            ],
            "prohibited_decisions": [
                "authorize action",
                "execute",
                "issue commands",
                "assess final threat",
                "override human authority",
                "determine operational response",
            ],
        }
