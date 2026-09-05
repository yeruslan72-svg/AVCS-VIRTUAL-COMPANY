"""
AVCS VIRTUAL COMPANY
State Machine — Operational Decision States

FUNCTION:
- Manage operational decision states
- Track state transitions
- Enforce decision pathway
- Maintain state history
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class OperationalState(Enum):
    """Operational decision states."""
    IDLE = "IDLE"
    EVENT_RECEIVED = "EVENT_RECEIVED"
    DISPATCHING = "DISPATCHING"
    DEPARTMENTS_PROCESSING = "DEPARTMENTS_PROCESSING"
    AGGREGATING = "AGGREGATING"
    CONFLICT_DETECTING = "CONFLICT_DETECTING"
    DECISION_FORMULATING = "DECISION_FORMULATING"
    AWAITING_AUTHORITY = "AWAITING_AUTHORITY"
    AUTHORIZED = "AUTHORIZED"
    REJECTED = "REJECTED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class StateMachine:
    """
    State Machine manages operational decision states.
    
    Responsibilities:
    - Track current state
    - Validate state transitions
    - Maintain state history
    - Enforce decision pathway
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.current_state = OperationalState.IDLE
        self.state_history = []
        self.event_id = None

    def start(self, event_id: str) -> Dict[str, Any]:
        """
        Start processing a new event.
        
        Args:
            event_id: Event ID
            
        Returns:
            State transition result
        """
        self.event_id = event_id
        return self._transition_to(OperationalState.EVENT_RECEIVED, f"Event received: {event_id}")

    def dispatch(self) -> Dict[str, Any]:
        """Transition to DISPATCHING state."""
        return self._transition_to(OperationalState.DISPATCHING, "Dispatching to Departments")

    def process(self) -> Dict[str, Any]:
        """Transition to DEPARTMENTS_PROCESSING state."""
        return self._transition_to(OperationalState.DEPARTMENTS_PROCESSING, "Departments processing")

    def aggregate(self) -> Dict[str, Any]:
        """Transition to AGGREGATING state."""
        return self._transition_to(OperationalState.AGGREGATING, "Aggregating results")

    def detect_conflicts(self) -> Dict[str, Any]:
        """Transition to CONFLICT_DETECTING state."""
        return self._transition_to(OperationalState.CONFLICT_DETECTING, "Detecting conflicts")

    def formulate_decision(self) -> Dict[str, Any]:
        """Transition to DECISION_FORMULATING state."""
        return self._transition_to(OperationalState.DECISION_FORMULATING, "Formulating decision proposal")

    def wait_for_authority(self) -> Dict[str, Any]:
        """Transition to AWAITING_AUTHORITY state."""
        return self._transition_to(OperationalState.AWAITING_AUTHORITY, "Awaiting human authority")

    def authorize(self) -> Dict[str, Any]:
        """Transition to AUTHORIZED state."""
        return self._transition_to(OperationalState.AUTHORIZED, "Decision authorized")

    def reject(self) -> Dict[str, Any]:
        """Transition to REJECTED state."""
        return self._transition_to(OperationalState.REJECTED, "Decision rejected")

    def execute(self) -> Dict[str, Any]:
        """Transition to EXECUTING state."""
        return self._transition_to(OperationalState.EXECUTING, "Executing authorized action")

    def complete(self) -> Dict[str, Any]:
        """Transition to COMPLETED state."""
        return self._transition_to(OperationalState.COMPLETED, "Decision cycle completed")

    def fail(self, reason: str) -> Dict[str, Any]:
        """Transition to FAILED state."""
        return self._transition_to(OperationalState.FAILED, f"Failed: {reason}")

    def _transition_to(self, new_state: OperationalState, message: str) -> Dict[str, Any]:
        """
        Perform a state transition.
        
        Args:
            new_state: Target state
            message: Transition description
            
        Returns:
            State transition result
        """
        old_state = self.current_state
        is_valid = self._is_valid_transition(old_state, new_state)

        # Record transition
        transition = {
            "event_id": self.event_id,
            "from_state": old_state.value,
            "to_state": new_state.value,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "message": message,
            "is_valid": is_valid
        }

        # Only update state if valid
        if is_valid:
            self.current_state = new_state
            transition["status"] = "SUCCESS"
        else:
            transition["status"] = "INVALID_TRANSITION"

        self.state_history.append(transition)

        self._log(f"State transition: {old_state.value} → {new_state.value} ({transition['status']})")

        return transition

    def _is_valid_transition(self, from_state: OperationalState, to_state: OperationalState) -> bool:
        """Validate state transitions."""
        # Define valid transitions
        valid_transitions = {
            OperationalState.IDLE: [OperationalState.EVENT_RECEIVED],
            OperationalState.EVENT_RECEIVED: [OperationalState.DISPATCHING],
            OperationalState.DISPATCHING: [OperationalState.DEPARTMENTS_PROCESSING],
            OperationalState.DEPARTMENTS_PROCESSING: [OperationalState.AGGREGATING],
            OperationalState.AGGREGATING: [OperationalState.CONFLICT_DETECTING],
            OperationalState.CONFLICT_DETECTING: [OperationalState.DECISION_FORMULATING],
            OperationalState.DECISION_FORMULATING: [OperationalState.AWAITING_AUTHORITY],
            OperationalState.AWAITING_AUTHORITY: [OperationalState.AUTHORIZED, OperationalState.REJECTED],
            OperationalState.AUTHORIZED: [OperationalState.EXECUTING],
            OperationalState.REJECTED: [OperationalState.IDLE, OperationalState.COMPLETED],
            OperationalState.EXECUTING: [OperationalState.COMPLETED],
            OperationalState.COMPLETED: [OperationalState.IDLE],
            OperationalState.FAILED: [OperationalState.IDLE],
        }
        
        if from_state in valid_transitions:
            return to_state in valid_transitions[from_state]
        return False

    def _log(self, message: str, level: str = "INFO"):
        """Simple logging for StateMachine."""
        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[{timestamp}] [STATE_MACHINE] [{level}] {message}")

    def get_state_history(self) -> List[Dict[str, Any]]:
        """Return the state history."""
        return self.state_history

    def get_current_state(self) -> str:
        """Return the current state."""
        return self.current_state.value

    def is_ready(self) -> bool:
        """Check if system is ready for a new event."""
        return self.current_state in [OperationalState.IDLE, OperationalState.COMPLETED, OperationalState.REJECTED]
