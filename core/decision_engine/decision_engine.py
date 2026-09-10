"""
AVCS VIRTUAL COMPANY
Decision Engine — Decision Proposal Generator

FUNCTION:
- Convert aggregated operational state into a structured Decision Proposal
- Respect North boundary (COMPASS veto)
- Use structural fields (north_status, stability_status, reality_status) to shape the proposal
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class DecisionEngine:
    """
    Decision Engine converts aggregated state into Decision Proposal.

    Principles:
    - North is non-negotiable. If COMPASS vetoes, no action proceeds.
    - Structural fields shape the proposal.
    - Recommendation is not authorization.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.decision_log = []

    def formulate(self, aggregated_state: Dict[str, Any], conflict_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formulate a Decision Proposal from aggregated state and conflict result.
        """
        event_id = aggregated_state.get("event_id", "UNKNOWN")
        self._log(f"Formulating decision proposal for event: {event_id}")

        # -------------------------------------------------------------------
        # Extract data
        # -------------------------------------------------------------------

        structural = aggregated_state.get("structural", {})
        north_status = structural.get("north_status")
        veto = structural.get("veto", False)
        stability_status = structural.get("stability_status")
        reality_status = structural.get("reality_status")
        structural_coherence = structural.get("structural_coherence")

        risk_assessment = aggregated_state.get("risk_assessment", {})
        overall_risk = risk_assessment.get("overall_risk", "LOW")
        risks = risk_assessment.get("risks", [])

        assessments = aggregated_state.get("assessments", {})
        evidence = aggregated_state.get("evidence", [])
        recommendations = aggregated_state.get("recommendations", [])
        uncertainty = aggregated_state.get("uncertainty", [])
        constraints = aggregated_state.get("constraints", [])

        has_conflict = conflict_result.get("has_conflicts", False)
        decision_blocked = conflict_result.get("decision_blocked", False)
        conflicts = conflict_result.get("conflicts", [])

        # -------------------------------------------------------------------
        # North boundary — non-negotiable
        # -------------------------------------------------------------------

        options: List[Dict[str, Any]] = []
        proposed_action: Optional[Dict[str, Any]] = None
        authority_required = "CAPTAIN Dpt."
        proposal_status = "PROPOSAL_READY"

        # If North is violated — no action may proceed
        if veto or north_status == "OUTSIDE NORTH":
            proposed_action = {
                "action": "NO_ACTION",
                "description": "Decision violates North — continuation prohibited",
                "risk": "CRITICAL",
            }
            options = [proposed_action]
            authority_required = "CAPTAIN Dpt. (North Violation)"
            proposal_status = "OUTSIDE_NORTH"

        # If North is undetermined — no action may proceed until requalification
        elif north_status == "UNDETERMINED":
            proposed_action = {
                "action": "HOLD",
                "description": "North not confirmed — requalification required before continuation",
                "risk": "HIGH",
            }
            options = [proposed_action]
            authority_required = "CAPTAIN Dpt. (North Requalification)"
            proposal_status = "NORTH_UNDETERMINED"

        # If stability is unstable — no action may proceed
        elif stability_status == "UNSTABLE":
            proposed_action = {
                "action": "HOLD",
                "description": "Environment unstable — action not supported",
                "risk": "HIGH",
            }
            options = [proposed_action]
            authority_required = "CAPTAIN Dpt. (Stability)"
            proposal_status = "UNSTABLE"

        # If reality is contradictory — no action may proceed
        elif reality_status == "CONTRADICTORY":
            proposed_action = {
                "action": "HOLD",
                "description": "Conflicting evidence — reality not established",
                "risk": "HIGH",
            }
            options = [proposed_action]
            authority_required = "CAPTAIN Dpt. (Reality)"
            proposal_status = "CONTRADICTORY"

        # If conflicts block the decision
        elif decision_blocked:
            proposed_action = {
                "action": "BLOCKED",
                "description": "Decision blocked due to conflicts",
                "risk": "HIGH",
            }
            options = [proposed_action]
            proposal_status = "BLOCKED"

        # -------------------------------------------------------------------
        # Risk-based proposal (only if North, stability, reality are acceptable)
        # -------------------------------------------------------------------

        else:
            if overall_risk == "CRITICAL":
                proposed_action = {
                    "action": "STOP_INTERVENTION",
                    "description": "Immediate intervention required — critical risk detected",
                    "risk": "CRITICAL",
                }
                options.append(proposed_action)
                options.append({
                    "action": "CHANGE_COURSE",
                    "description": "Adjust course to avoid critical area",
                    "risk": "HIGH",
                })
                options.append({
                    "action": "MONITOR",
                    "description": "Continue monitoring with increased attention",
                    "risk": "MEDIUM",
                })
                authority_required = "CAPTAIN Dpt. (Immediate)"

            elif overall_risk == "HIGH":
                proposed_action = {
                    "action": "CHANGE_COURSE",
                    "description": "High risk detected — course adjustment recommended",
                    "risk": "HIGH",
                }
                options.append(proposed_action)
                options.append({
                    "action": "MONITOR",
                    "description": "Continue monitoring with increased attention",
                    "risk": "MEDIUM",
                })
                options.append({
                    "action": "CONTINUE",
                    "description": "Continue with caution",
                    "risk": "LOW",
                })
                authority_required = "CAPTAIN Dpt. (Immediate)"

            else:
                proposed_action = {
                    "action": "CONTINUE",
                    "description": "Continue observation",
                    "risk": "LOW",
                }
                options.append(proposed_action)
                options.append({
                    "action": "MONITOR",
                    "description": "Continue standard monitoring",
                    "risk": "LOW",
                })
                authority_required = "CAPTAIN Dpt."

        # -------------------------------------------------------------------
        # Build Decision Proposal
        # -------------------------------------------------------------------

        decision_proposal = {
            "event_id": event_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "operational_state": {
                "assessments": assessments,
                "constraints": constraints,
                "uncertainty": uncertainty,
            },
            "structural": {
                "north_status": north_status,
                "veto": veto,
                "stability_status": stability_status,
                "reality_status": reality_status,
                "structural_coherence": structural_coherence,
            },
            "evidence": evidence,
            "risks": risks,
            "recommendations": recommendations,
            "available_options": options,
            "constraints": constraints,
            "conflicts": conflicts,
            "has_conflict": has_conflict,
            "decision_blocked": decision_blocked,
            "authority_required": authority_required,
            "proposed_action": proposed_action,
            "status": proposal_status,
            "risk_assessment": risk_assessment,
        }

        self.decision_log.append(decision_proposal)
        return decision_proposal

    def _log(self, message: str, level: str = "INFO"):
        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[{timestamp}] [DECISION_ENGINE] [{level}] {message}")

    def get_decision_log(self) -> List[Dict[str, Any]]:
        return self.decision_log
