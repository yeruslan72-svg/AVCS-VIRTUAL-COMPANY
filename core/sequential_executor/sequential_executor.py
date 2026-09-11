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

    Order:
    1. LOOKOUT   — foresight, signals, trends
    2. CHARTS    — structured reality, facts
    3. GYRO      — stability, load
    4. NAVIGATOR — strategy, course
    5. COMPASS   — North check (receives course from NAVIGATOR)
    6. HELM      — decision (receives north_status, stability, reality)
    7. CAPTAIN   — review (receives ALL department results)
    """

    # Structural fields to accumulate between departments
    STRUCTURAL_KEYS = [
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

        self.event_id: Optional[str] = None
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
        Execute departments sequentially.

        CAPTAIN is executed LAST, after all other departments,
        because it needs the full department_results for review.
        """
        # 1. Execute all departments EXCEPT CAPTAIN
        for dept in self.departments:
            dept_name = dept.department_name

            # Skip CAPTAIN — will be executed separately at the end
            if "CAPTAIN" in dept_name.upper():
                continue

            # Build input: event_data + accumulated_state + event_id
            dept_input = {
                **event_data,
                **self.accumulated_state,
                "event_id": self.event_id,
            }

            # Special handling: COMPASS needs decision_proposal
            # (from NAVIGATOR course, since course IS the intent)
            if "COMPASS" in dept_name.upper():
                if "decision_proposal" not in dept_input:
                    # Use course from NAVIGATOR as decision_proposal (intent)
                    if "course" in self.accumulated_state:
                        dept_input["decision_proposal"] = self.accumulated_state["course"]
                    else:
                        dept_input["decision_proposal"] = None

            self._log(f"Executing {dept_name}")

            try:
                result = dept.process(dept_input)
            except Exception as e:
                self._log(f"{dept_name} failed: {e}", level="ERROR")
                result = self._error_result(dept_name, str(e))

            # Verify event_id
            self._verify_event_id(dept_name, result)

            # Store result
            self.department_results[dept_name] = result

            # Accumulate structural fields
            self._accumulate_state(dept_name, result)

            # Log
            self._log_department(dept_name, result)

        # 2. Execute CAPTAIN separately — with full department_results
        captain = self._find_department("CAPTAIN")
        if captain is not None:
            captain_name = captain.department_name

            captain_input = {
                **event_data,
                **self.accumulated_state,
                "event_id": self.event_id,
                "department_assessments": self.department_results,
                "north_status": self.accumulated_state.get("north_status"),
                "decision_state": self.accumulated_state.get("decision_state"),
                "conflict_result": {},  # Conflict detection happens after
                "authority_state": None,  # Authority happens after
            }

            self._log(f"Executing {captain_name} (with full department results)")

            try:
                result = captain.process(captain_input)
            except Exception as e:
                self._log(f"{captain_name} failed: {e}", level="ERROR")
                result = self._error_result(captain_name, str(e))

            self._verify_event_id(captain_name, result)
            self.department_results[captain_name] = result
            self._accumulate_state(captain_name, result)
            self._log_department(captain_name, result)

    def _find_department(self, keyword: str):
        """Find a department by keyword in its name."""
        for dept in self.departments:
            if keyword.upper() in dept.department_name.upper():
                return dept
        return None

    def _verify_event_id(self, dept_name: str, result: Dict[str, Any]) -> None:
        """Verify event_id consistency in department result."""
        if result.get("event_id") != self.event_id:
            self._log(
                f"EVENT_ID MISMATCH in {dept_name}: "
                f"expected {self.event_id}, got {result.get('event_id')}",
                level="ERROR"
            )
            result["event_id"] = self.event_id

    def _error_result(self, dept_name: str, error: str) -> Dict[str, Any]:
        """Create a standard error result for a failed department."""
        return {
            "department": dept_name,
            "event_id": self.event_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "assessment": f"FAILED: {error}",
            "evidence": [],
            "confidence": 0.0,
            "uncertainty": [error],
            "constraints": [],
            "recommendations": [],
            "authority_state": "UNKNOWN",
            "status": "FAILED",
        }

    def _accumulate_state(self, dept_name: str, result: Dict[str, Any]) -> None:
        """Accumulate structural fields from department result into state."""
        for key in self.STRUCTURAL_KEYS:
            if key in result and result[key] is not None:
                self.accumulated_state[key] = result[key]

        # Also accumulate raw department output for cross-reference
        self.accumulated_state[f"_{dept_name}_result"] = result

    def _log_department(self, dept_name: str, result: Dict[str, Any]) -> None:
        """Log department execution."""
        self.execution_log.append({
            "department": dept_name,
            "event_id": self.event_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": result.get("status", "UNKNOWN"),
            "authority_state": result.get("authority_state"),
        })

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
