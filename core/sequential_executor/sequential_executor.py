"""
AVCS VIRTUAL COMPANY
Sequential Executor — Constitution-Aligned Orchestrator

FUNCTION:
- Own the event lifecycle (one event_id per cycle)
- Execute departments in Constitution-defined order
- Accumulate state between departments
- Pass accumulated state to each subsequent department
- Synchronize with StateMachine for logging
- Coordinate Aggregation, Conflict Detection, Decision, Authority

ORDER (Constitution-aligned):
LOOKOUT → CHARTS → GYRO → NAVIGATOR → COMPASS → HELM → CAPTAIN

PRINCIPLE:
Code must implement the Constitution — not redefine it.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid


class SequentialExecutor:
    """
    SequentialExecutor orchestrates the decision cycle.

    It replaces parallel fan-out (Dispatcher) with sequential dependency.

    Each department receives:
    - event_data (original incident)
    - accumulated_state (outputs from previous departments)
    - event_id (single, authoritative)

    Each department returns:
    - structured response (via BaseDepartment._create_response)
    - structural fields (via **kwargs)
    """

    def __init__(
        self,
        departments: List,
        state_machine,
        aggregator,
        conflict_detector,
        decision_engine,
        authority_gate,
        config: Optional[Dict[str, Any]] = None
    ):
        self.departments = departments
        self.state_machine = state_machine
        self.aggregator = aggregator
        self.conflict_detector = conflict_detector
        self.decision_engine = decision_engine
        self.authority_gate = authority_gate
        self.config = config or {}

        self.event_id = None
        self.accumulated_state: Dict[str, Any] = {}
        self.department_results: Dict[str, Any] = {}
        self.execution_log: List[Dict[str, Any]] = []

    # -------------------------------------------------------------------
    # PUBLIC API
    # -------------------------------------------------------------------

    def execute(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute full decision cycle sequentially.

        Args:
            event_data: Original incident data

        Returns:
            Full cycle result with department_results, aggregated_state,
            conflict_result, decision_proposal, authority_state, state_history
        """
        # 1. Own the event_id
        self.event_id = event_data.get("event_id") or self._generate_event_id()
        event_data = {**event_data, "event_id": self.event_id}

        self._log(f"Sequential execution started — event: {self.event_id}")

        # 2. Start state machine
        self.state_machine.start(self.event_id)

        # 3. Dispatch (log)
        self.state_machine.dispatch()

        # 4. Process departments
        self.state_machine.process()
        self._execute_departments(event_data)

        # 5. Aggregate
        self.state_machine.aggregate()
        aggregated_state = self.aggregator.aggregate(
            self.department_results, self.event_id
        )

        # 6. Detect conflicts
        self.state_machine.detect_conflicts()
        conflict_result = self.conflict_detector.detect(aggregated_state)

        # 7. Formulate decision
        self.state_machine.formulate_decision()
        decision_proposal = self.decision_engine.formulate(
            aggregated_state, conflict_result
        )

        # 8. Present to authority gate
        self.state_machine.wait_for_authority()
        authority_state = self.authority_gate.present_decision(decision_proposal)

        # 9. Build result
        result = {
            "event_id": self.event_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "department_results": self.department_results,
            "aggregated_state": aggregated_state,
            "conflict_result": conflict_result,
            "decision_proposal": decision_proposal,
            "authority_state": authority_state,
            "state_history": self.state_machine.get_state_history(),
            "execution_log": self.execution_log,
        }

        self._log(f"Sequential execution completed — event: {self.event_id}")
        return result

    # -------------------------------------------------------------------
    # INTERNAL: Department execution
    # -------------------------------------------------------------------

    def _execute_departments(self, event_data: Dict[str, Any]) -> None:
        """
        Execute departments sequentially, accumulating state.
        """
        for dept in self.departments:
            dept_name = dept.department_name

            # Build input: event_data + accumulated_state + event_id
            dept_input = {
                **event_data,
                **self.accumulated_state,
                "event_id": self.event_id,
            }

            self._log(f"Executing {dept_name}")

            try:
                result = dept.process(dept_input)
            except Exception as e:
                self._log(f"{dept_name} failed: {e}", level="ERROR")
                result = {
                    "department": dept_name,
                    "event_id": self.event_id,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "assessment": f"FAILED: {e}",
                    "evidence": [],
                    "confidence": 0.0,
                    "uncertainty": [str(e)],
                    "constraints": [],
                    "recommendations": [],
                    "authority_state": getattr(dept, "authority_state", "UNKNOWN"),
                    "status": "FAILED",
                }

            # Verify event_id consistency
            if result.get("event_id") != self.event_id:
                self._log(
                    f"EVENT_ID MISMATCH in {dept_name}: "
                    f"expected {self.event_id}, got {result.get('event_id')}",
                    level="ERROR"
                )
                result["event_id"] = self.event_id

            # Store result
            self.department_results[dept_name] = result

            # Accumulate structural fields into state
            self._accumulate_state(dept_name, result)

            # Log
            self.execution_log.append({
                "department": dept_name,
                "event_id": self.event_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": result.get("status", "UNKNOWN"),
                "authority_state": result.get("authority_state"),
            })

    def _accumulate_state(self, dept_name: str, result: Dict[str, Any]) -> None:
        """
        Accumulate structural fields from department result into state.

        These fields become available to subsequent departments.
        """
        # Structural fields to accumulate
        structural_keys = [
            # LOOKOUT
            "signal_state", "trajectory", "signals", "trends", "deviations",
            # CHARTS
            "reality_status", "reality_confidence", "facts", "unknowns",
            "contradictions", "assumptions",
            # GYRO
            "stability_status", "load_level", "human_condition",
            "system_condition", "risk_factors",
            # NAVIGATOR
            "course", "course_state", "anticipated_changes",
            # COMPASS
            "north_status", "veto",
            # HELM
            "decision", "decision_state", "basis",
            # CAPTAIN
            "structural_coherence", "role_integrity", "north_integrity",
            "decision_quality", "recommendation", "findings",
        ]

        for key in structural_keys:
            if key in result and result[key] is not None:
                self.accumulated_state[key] = result[key]

        # Also accumulate raw department outputs for cross-reference
        self.accumulated_state[f"_{dept_name}_result"] = result

    # -------------------------------------------------------------------
    # UTILITIES
    # -------------------------------------------------------------------

    def _generate_event_id(self) -> str:
        """Generate a unique event ID (only if not provided)."""
        return f"EVT-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"

    def _log(self, message: str, level: str = "INFO") -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        print(f"[{timestamp}] [SEQUENTIAL_EXECUTOR] [{level}] {message}")

    def get_execution_log(self) -> List[Dict[str, Any]]:
        return self.execution_log
