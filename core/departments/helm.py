"""
AVCS VIRTUAL COMPANY
HELM Dpt. — Execution Readiness and Execution Control

CONTRACT:
PURPOSE: Determine execution readiness and perform authorized operational execution
AUTHORITY: EXECUTION ONLY
PROHIBITED: Create independent operational objectives, authorize its own command, execute unauthorized action
"""

from typing import Dict, Any, List
from datetime import datetime
from core.departments.base import BaseDepartment


class HelmDepartment(BaseDepartment):
    """
    HELM Dpt. — Execution Readiness and Execution Control.
    
    Responsibilities:
    - Assess execution feasibility
    - Identify execution constraints
    - Verify system readiness
    - Execute an authorized command
    - Report execution status
    - Confirm execution result
    """

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("HELM Dpt.", config)
        self.authority_state = "EXECUTION_ONLY"
        self.ready = False
        self.executed_commands = []

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming data and assess execution readiness.
        
        Required input fields:
        - action: Action to execute or assess
        - authorized: Whether the action is authorized (bool)
        - system_status: Current system status
        """
        # Validate input
        required_fields = ["action", "authorized"]
        if not self._validate_input(input_data, required_fields):
            self._log("Missing required fields in input", "WARNING")
            return self._create_response(
                assessment="INVALID INPUT — Missing required fields",
                evidence=[],
                confidence=0.0,
                uncertainty=["Required fields: action, authorized"],
                status="FAILED"
            )

        # Extract data
        action = input_data.get("action")
        authorized = input_data.get("authorized", False)
        system_status = input_data.get("system_status", "nominal")
        constraints = input_data.get("constraints", [])

        # Generate event ID if not provided
        self.event_id = input_data.get("event_id") or self._generate_event_id()

        self._log(f"Processing execution readiness: action='{action}', authorized={authorized}")

        # Determine readiness
        readiness = "READY"
        if system_status != "nominal":
            readiness = "DEGRADED"
        if constraints:
            readiness = "CONSTRAINED"
        
        # Determine if can execute
        can_execute = authorized and readiness == "READY"
        execution_result = None

        # Build evidence
        evidence = [
            f"Action: {action}",
            f"Authorization: {'YES' if authorized else 'NO'}",
            f"System status: {system_status}",
            f"Readiness: {readiness}",
            f"Can execute: {'YES' if can_execute else 'NO'}"
        ]

        # If authorized and ready, execute
        execution_status = "NOT_EXECUTED"
        if can_execute:
            execution_status = "EXECUTED"
            execution_time = datetime.utcnow().isoformat() + "Z"
            self.executed_commands.append({
                "action": action,
                "time": execution_time,
                "status": "SUCCESS"
            })
            execution_result = f"Action '{action}' executed at {execution_time}"
            evidence.append(f"Execution time: {execution_time}")
        elif authorized and readiness != "READY":
            execution_status = "BLOCKED"
            evidence.append(f"Execution blocked: readiness={readiness}")
            if constraints:
                evidence.append(f"Constraints: {', '.join(constraints)}")

        # Build uncertainty
        uncertainty = []
        if not authorized:
            uncertainty.append("Action not authorized — execution required CAPTAIN Dpt. approval")
        if readiness != "READY":
            uncertainty.append(f"System readiness: {readiness}")

        # Build recommendations
        recommendations = []
        if not authorized:
            recommendations.append("Obtain CAPTAIN Dpt. authorization")
        if readiness != "READY":
            recommendations.append(f"Resolve system issues: {readiness}")
        if authorized and readiness == "READY" and not can_execute:
            recommendations.append("Check execution conditions")
        if can_execute:
            recommendations.append("Execute authorized action")

        return self._create_response(
            assessment=f"Execution readiness: {readiness}",
            evidence=evidence,
            confidence=0.90 if can_execute else 0.60,
            uncertainty=uncertainty,
            constraints=constraints,
            recommendations=recommendations,
            status=execution_status,
            event_id=self.event_id,
            readiness=readiness,
            can_execute=can_execute,
            authorized=authorized,
            execution_result=execution_result,
            action=action
        )

    def get_contract(self) -> Dict[str, Any]:
        """Return the HELM Dpt. contract."""
        return {
            "department": self.department_name,
            "purpose": "Determine execution readiness and perform authorized operational execution",
            "authority": "EXECUTION_ONLY",
            "prohibited_decisions": [
                "create independent operational objectives",
                "authorize its own command",
                "execute an unauthorized action",
                "suppress execution failure",
                "redefine an authorized command without authority"
            ],
            "permitted_recommendations": [
                "execution feasibility",
                "alternative execution method",
                "delay due to technical limitation",
                "technical constraint requiring CAPTAIN review"
            ]
        }
