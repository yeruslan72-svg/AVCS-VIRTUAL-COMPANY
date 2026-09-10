"""
AVCS VIRTUAL COMPANY
LOOKOUT Dpt. — Foresight & Anticipation

CONTRACT:
PURPOSE: Detect weak signals, anticipate change, and identify early deviation indicators.
AUTHORITY: SIGNAL_AUTHORITY.
PROHIBITED: Authorize action, execute, issue commands, determine final threat, suppress signals.
"""

from typing import Dict, Any, List
from datetime import datetime, timezone
from core.departments.base import BaseDepartment


class LookoutDepartment(BaseDepartment):
    """
    LOOKOUT Dpt. — Foresight & Anticipation.

    LOOKOUT does not authorize.
    LOOKOUT does not execute.
    LOOKOUT does not determine final threat.

    LOOKOUT detects weak signals.
    LOOKOUT anticipates change.
    LOOKOUT identifies early deviation indicators.

    Good navigation begins before the storm appears.
    """

    SIGNAL_STATES = {
        "SIGNAL_DETECTED": "a weak signal has been detected",
        "TREND_EMERGING": "a pattern is emerging across multiple signals",
        "DEVIATION_INDICATED": "an early deviation indicator has been identified",
        "NO_SIGNAL": "no signal detected",
        "UNDETERMINED": "signal status cannot be determined",
    }

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("LOOKOUT Dpt.", config)
        self.authority_state = "SIGNAL_AUTHORITY"

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect weak signals and anticipate change.

        Required input fields:
        - observations: list of observed signals (optional)
        - trends: list of emerging trends (optional)
        - deviations: list of early deviation indicators (optional)
        - context: broader operational context (optional)

        Returns:
        - signals: detected weak signals
        - trends: emerging trends
        - deviations: early deviation indicators
        - signal_state: SIGNAL_DETECTED / TREND_EMERGING / DEVIATION_INDICATED / NO_SIGNAL / UNDETERMINED
        - trajectory: anticipated trajectory of change
        """

        observations = input_data.get("observations", [])
        trends = input_data.get("trends", [])
        deviations = input_data.get("deviations", [])
        context = input_data.get("context", {})

        self.event_id = input_data.get("event_id") or self._generate_event_id()

        self._log(
            f"LOOKOUT foresight scan — "
            f"observations={len(observations)}, "
            f"trends={len(trends)}, "
            f"deviations={len(deviations)}"
        )

        # -------------------------------------------------------------------
        # Foresight and anticipation — weak signals, not final threat
        # -------------------------------------------------------------------

        evidence: List[str] = []
        uncertainty: List[str] = []
        trajectory: List[str] = []

        # Observations
        if observations:
            for obs in observations:
                evidence.append(f"OBSERVATION: {obs}")
        else:
            uncertainty.append("No observations provided")

        # Trends
        if trends:
            for trend in trends:
                evidence.append(f"TREND: {trend}")
        else:
            uncertainty.append("No emerging trends provided")

        # Deviations
        if deviations:
            for dev in deviations:
                evidence.append(f"DEVIATION: {dev}")
        else:
            uncertainty.append("No early deviation indicators provided")

        # Context
        if context:
            for key, value in context.items():
                evidence.append(f"CONTEXT — {key}: {value}")
        else:
            uncertainty.append("No operational context provided")

        # Trajectory anticipation
        if deviations:
            trajectory.append(
                "Deviation indicators suggest boundary movement"
            )
        if trends:
            trajectory.append(
                f"{len(trends)} trends suggest direction of change"
            )
        if not trajectory:
            trajectory.append("No clear trajectory anticipated")

        # -------------------------------------------------------------------
        # Determine signal state — structural, not interpretive
        # -------------------------------------------------------------------

        if deviations:
            signal_state = "DEVIATION_INDICATED"
            assessment = (
                f"DEVIATION INDICATED — {len(deviations)} early "
                "deviation indicators identified"
            )
        elif trends:
            signal_state = "TREND_EMERGING"
            assessment = (
                f"TREND EMERGING — {len(trends)} trends identified"
            )
        elif observations:
            signal_state = "SIGNAL_DETECTED"
            assessment = (
                f"SIGNAL DETECTED — {len(observations)} observations"
            )
        elif not observations and not trends and not deviations:
            signal_state = "NO_SIGNAL"
            assessment = "NO SIGNAL — no weak signals detected"
        else:
            signal_state = "UNDETERMINED"
            assessment = "UNDETERMINED — signal status unclear"

        # -------------------------------------------------------------------
        # Response
        # -------------------------------------------------------------------

        return self._create_response(
            assessment=assessment,
            evidence=evidence,
            confidence=0.85 if signal_state == "DEVIATION_INDICATED"
                       else 0.80 if signal_state == "TREND_EMERGING"
                       else 0.75 if signal_state == "SIGNAL_DETECTED"
                       else 0.60,
            uncertainty=uncertainty,
            constraints=[],
            recommendations=[],
            status="COMPLETED",
            event_id=self.event_id,
            signal_state=signal_state,
            signals=observations,
            trends=trends,
            deviations=deviations,
            trajectory=trajectory,
            authority_state=self.authority_state,
        )

    def get_contract(self) -> Dict[str, Any]:
        """Return the LOOKOUT Dpt. contract — Foresight & Anticipation."""
        return {
            "department": self.department_name,
            "purpose": "Detect weak signals, anticipate change, and identify early deviation indicators.",
            "authority": "SIGNAL_AUTHORITY",
            "question": "What is changing?",
            "signal_states": self.SIGNAL_STATES,
            "permitted_outputs": [
                "SIGNAL_DETECTED",
                "TREND_EMERGING",
                "DEVIATION_INDICATED",
                "NO_SIGNAL",
                "UNDETERMINED",
            ],
            "prohibited_decisions": [
                "authorize action",
                "execute",
                "issue commands",
                "determine final threat",
                "suppress signals",
                "interpret North",
            ],
        }
