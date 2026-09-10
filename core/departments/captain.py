"""
AVCS VIRTUAL COMPANY
CAPTAIN Dpt. — System Integration & Review

CONTRACT:
PURPOSE: Ensure the structural coherence of the decision system.
AUTHORITY: REVIEW_AUTHORITY.
PROHIBITED: Authorize, execute, issue commands, replace human authority, interpret North.
"""

from typing import Dict, Any, List
from datetime import datetime, timezone
from core.departments.base import BaseDepartment


class CaptainDepartment(BaseDepartment):
    """
    CAPTAIN Dpt. — System Integration & Review.

    CAPTAIN does not authorize.
    CAPTAIN does not execute.
    CAPTAIN does not issue commands.
    CAPTAIN does not replace human authority.

    CAPTAIN reviews whether the system itself remained structurally coherent
    throughout the decision cycle.

    A captain does not steer the ship.
    A captain ensures the ship remains a ship.
    """

    COHERENCE_STATES = {
        "INTACT": "the system remained structurally coherent",
        "CONDITIONALLY_INTACT": "the system remained coherent with limitations",
        "FRAGMENTED": "the system lost structural coherence",
        "BROKEN": "the system failed structurally",
    }

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("CAPTAIN Dpt.", config)
        self.authority_state = "REVIEW_AUTHORITY"

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review whether the system remained structurally coherent.

        Required input fields:
        - department_assessments: dict of all department outputs
        - north_status: WITHIN / OUTSIDE / UNDETERMINED (from COMPASS)
        - decision_state: result from HELM
        - conflict_result: result of conflict detection (optional)
        - authority_state: state of authority boundary (optional)

        Returns:
        - structural_coherence: INTACT / CONDITIONALLY INTACT / FRAGMENTED / BROKEN
        - role_integrity: assessment of role separation
        - north_integrity: assessment of North compliance
        - decision_quality: assessment of decision process
        - recommendation: NO ACTION / MONITOR / REVIEW / ESCALATE / RECONFIGURE
        """

        department_assessments = input_data.get("department_assessments", {})
        north_status = input_data.get("north_status")
        decision_state = input_data.get("decision_state")
        conflict_result = input_data.get("conflict_result", {})
        authority_state = input_data.get("authority_state")

        self.event_id = input_data.get("event_id") or self._generate_event_id()

        self._log(
            f"CAPTAIN structural review — north={north_status}, "
            f"decision={decision_state}, "
            f"departments={len(department_assessments)}"
        )

        # -------------------------------------------------------------------
        # Structural review — coherence, not authority
        # -------------------------------------------------------------------

        evidence: List[str] = []
        uncertainty: List[str] = []
        findings: List[str] = []

        # 1. Role integrity — did each department remain in its role?
        role_integrity = "INTACT"
        evidence.append(
            f"Departments reviewed: {len(department_assessments)}"
        )
        for dept_name, dept_output in department_assessments.items():
            if not isinstance(dept_output, dict):
                findings.append(f"{dept_name}: output not structured")
                role_integrity = "CONDITIONALLY INTACT"
                continue
            if "error" in dept_output:
                findings.append(
                    f"{dept_name}: failed — {dept_output['error']}"
                )
                role_integrity = "CONDITIONALLY INTACT"
            else:
                evidence.append(f"{dept_name}: completed")

        # 2. North integrity — was North applied, not interpreted?
        if north_status == "OUTSIDE NORTH":
            north_integrity = "BROKEN"
            findings.append("North violation detected")
        elif north_status == "UNDETERMINED":
            north_integrity = "FRAGMENTED"
            findings.append("North status undetermined")
        elif north_status == "WITHIN NORTH":
            north_integrity = "INTACT"
            evidence.append("North: applied correctly")
        else:
            north_integrity = "UNDETERMINED"
            uncertainty.append("North status not provided")

        # 3. Decision quality — was a decision made within structural support?
        if decision_state == "DECISION_MADE":
            decision_quality = "INTACT"
            evidence.append("Decision: made within structural support")
        elif decision_state in ("DEFERRED", "ESCALATED"):
            decision_quality = "CONDITIONALLY INTACT"
            findings.append(f"Decision: {decision_state}")
        elif decision_state == "NO_DECISION":
            decision_quality = "FRAGMENTED"
            findings.append("Decision: no decision could be made")
        else:
            decision_quality = "UNDETERMINED"
            uncertainty.append("Decision state not provided")

        # 4. Conflict handling — were conflicts resolved or visible?
        if conflict_result.get("has_conflicts"):
            if conflict_result.get("decision_blocked"):
                evidence.append("Conflicts: detected and blocked execution")
            else:
                findings.append("Conflicts: detected but not blocked")
        else:
            evidence.append("Conflicts: none detected")

        # 5. Authority boundary — was human authority respected?
        if authority_state == "HUMAN_AUTHORITY_REQUIRED":
            evidence.append("Authority: human authority required")
        elif authority_state == "AUTHORIZED":
            evidence.append("Authority: human authorization received")
        elif authority_state is None:
            uncertainty.append("Authority state not provided")
        else:
            evidence.append(f"Authority state: {authority_state}")

        # -------------------------------------------------------------------
        # Determine structural coherence
        # -------------------------------------------------------------------

        if role_integrity == "INTACT" and north_integrity == "INTACT" and decision_quality == "INTACT":
            structural_coherence = "INTACT"
            recommendation = "NO ACTION"
            assessment = (
                "INTACT — system remained structurally coherent"
            )
        elif "BROKEN" in (role_integrity, north_integrity, decision_quality):
            structural_coherence = "BROKEN"
            recommendation = "RECONFIGURE"
            assessment = (
                "BROKEN — structural failure detected: "
                + "; ".join(findings)
            )
        elif "FRAGMENTED" in (role_integrity, north_integrity, decision_quality):
            structural_coherence = "FRAGMENTED"
            recommendation = "ESCALATE"
            assessment = (
                "FRAGMENTED — structural coherence lost: "
                + "; ".join(findings)
            )
        elif findings:
            structural_coherence = "CONDITIONALLY INTACT"
            recommendation = "REVIEW"
            assessment = (
                "CONDITIONALLY INTACT — limitations detected: "
                + "; ".join(findings)
            )
        else:
            structural_coherence = "CONDITIONALLY INTACT"
            recommendation = "MONITOR"
            assessment = (
                "CONDITIONALLY INTACT — some data incomplete"
            )

        # -------------------------------------------------------------------
        # Response
        # -------------------------------------------------------------------

        return self._create_response(
            assessment=assessment,
            evidence=evidence,
            confidence=0.90 if structural_coherence == "INTACT"
                       else 0.85 if structural_coherence == "BROKEN"
                       else 0.70,
            uncertainty=uncertainty,
            constraints=findings,
            recommendations=[recommendation],
            status="COMPLETED",
            event_id=self.event_id,
            structural_coherence=structural_coherence,
            role_integrity=role_integrity,
            north_integrity=north_integrity,
            decision_quality=decision_quality,
            recommendation=recommendation,
            findings=findings,
            authority_state=self.authority_state,
        )

    def get_contract(self) -> Dict[str, Any]:
        """Return the CAPTAIN Dpt. contract — System Integration & Review."""
        return {
            "department": self.department_name,
            "purpose": "Ensure the structural coherence of the decision system.",
            "authority": "REVIEW_AUTHORITY",
            "question": "Did the system remain structurally coherent?",
            "coherence_states": self.COHERENCE_STATES,
            "permitted_outputs": [
                "INTACT",
                "CONDITIONALLY INTACT",
                "FRAGMENTED",
                "BROKEN",
            ],
            "permitted_recommendations": [
                "NO ACTION",
                "MONITOR",
                "REVIEW",
                "ESCALATE",
                "RECONFIGURE",
            ],
            "prohibited_decisions": [
                "authorize action",
                "execute",
                "issue commands",
                "replace human authority",
                "interpret North",
                "change North",
                "become a hidden CEO",
            ],
        }
