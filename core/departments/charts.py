"""
AVCS VIRTUAL COMPANY
CHARTS Dpt. — Structured Reality

CONTRACT:
PURPOSE: Establish and maintain an accurate, structured representation of operational reality.
AUTHORITY: Fact Authority / Evidence Authority.
PROHIBITED: Recommend actions, authorize maneuvers, interpret facts, predict the future.
"""

from typing import Dict, Any, List
from datetime import datetime, timezone
from core.departments.base import BaseDepartment


class ChartsDepartment(BaseDepartment):
    """
    CHARTS Dpt. — Structured Reality.

    CHARTS does not recommend actions.
    CHARTS does not authorize maneuvers.
    CHARTS does not interpret facts.
    CHARTS does not predict the future.

    CHARTS establishes what is fact.

    A chart is not an opinion.
    A chart is a structured representation of reality.
    """

    REALITY_CATEGORIES = {
        "FACT": "observable, documented, verifiable",
        "OBSERVATION": "what has been noticed",
        "ASSUMPTION": "what is assumed",
        "UNKNOWN": "what is not known",
        "CONTRADICTION": "conflicting evidence",
    }

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("CHARTS Dpt.", config)
        self.authority_state = "FACT_AUTHORITY"

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Establish structured reality from incoming data.

        Required input fields:
        - facts: list of observed/verifiable facts (optional)
        - observations: list of what has been noticed (optional)
        - assumptions: list of what is assumed (optional)
        - unknowns: list of what is not known (optional)
        - contradictions: list of conflicting evidence (optional)

        Returns:
        - facts: established facts
        - observations: documented observations
        - assumptions: stated assumptions
        - unknowns: identified unknowns
        - contradictions: identified contradictions
        - confidence: HIGH / MEDIUM / LOW
        """

        facts = input_data.get("facts", [])
        observations = input_data.get("observations", [])
        assumptions = input_data.get("assumptions", [])
        unknowns = input_data.get("unknowns", [])
        contradictions = input_data.get("contradictions", [])

        self.event_id = input_data.get("event_id") or self._generate_event_id()

        self._log(
            f"CHARTS reality check — "
            f"facts={len(facts)}, observations={len(observations)}, "
            f"assumptions={len(assumptions)}, unknowns={len(unknowns)}, "
            f"contradictions={len(contradictions)}"
        )

        # -------------------------------------------------------------------
        # Structured reality assessment — fact discipline
        # -------------------------------------------------------------------

        evidence: List[str] = []
        uncertainty: List[str] = []

        # Facts
        if facts:
            evidence.append(f"Facts established: {len(facts)}")
            for fact in facts:
                evidence.append(f"FACT: {fact}")
        else:
            uncertainty.append("No established facts provided")

        # Observations
        if observations:
            evidence.append(f"Observations documented: {len(observations)}")
            for obs in observations:
                evidence.append(f"OBSERVATION: {obs}")

        # Assumptions
        if assumptions:
            for asm in assumptions:
                evidence.append(f"ASSUMPTION: {asm}")
                uncertainty.append(f"Unverified assumption: {asm}")

        # Unknowns
        if unknowns:
            for unk in unknowns:
                evidence.append(f"UNKNOWN: {unk}")
                uncertainty.append(f"Unknown: {unk}")

        # Contradictions
        if contradictions:
            for con in contradictions:
                evidence.append(f"CONTRADICTION: {con}")
            uncertainty.append(
                f"Contradictions detected: {len(contradictions)}"
            )

        # -------------------------------------------------------------------
        # Determine reality status — structural, not interpretive
        # -------------------------------------------------------------------

        if contradictions:
            reality_status = "CONTRADICTORY"
            confidence = "LOW"
            assessment = (
                "CONTRADICTION — conflicting evidence detected: "
                + "; ".join(contradictions)
            )
        elif not facts and not observations:
            reality_status = "UNDETERMINED"
            confidence = "LOW"
            assessment = (
                "UNDETERMINED — no facts or observations provided"
            )
        elif not facts:
            reality_status = "PARTIAL"
            confidence = "MEDIUM"
            assessment = (
                "PARTIAL — observations exist, no verified facts"
            )
        else:
            reality_status = "STRUCTURED"
            confidence = "HIGH"
            assessment = (
                f"STRUCTURED — {len(facts)} facts established, "
                f"{len(unknowns)} unknowns, "
                f"{len(assumptions)} assumptions"
            )

        # -------------------------------------------------------------------
        # Response
        # -------------------------------------------------------------------

        return self._create_response(
            assessment=assessment,
            evidence=evidence,
            confidence=0.95 if confidence == "HIGH"
                       else 0.75 if confidence == "MEDIUM"
                       else 0.60,
            uncertainty=uncertainty,
            constraints=[],
            recommendations=[],  # CHARTS does not recommend actions
            status="COMPLETED",
            event_id=self.event_id,
            reality_status=reality_status,
            facts=facts,
            observations=observations,
            assumptions=assumptions,
            unknowns=unknowns,
            contradictions=contradictions,
            reality_confidence=confidence,
            authority_state=self.authority_state,
        )

    def get_contract(self) -> Dict[str, Any]:
        """Return the CHARTS Dpt. contract — Structured Reality."""
        return {
            "department": self.department_name,
            "purpose": "Establish and maintain an accurate, structured representation of operational reality.",
            "authority": "FACT_AUTHORITY / EVIDENCE_AUTHORITY",
            "question": "What do we actually know?",
            "reality_categories": self.REALITY_CATEGORIES,
            "permitted_outputs": [
                "FACT",
                "OBSERVATION",
                "ASSUMPTION",
                "UNKNOWN",
                "CONTRADICTION",
            ],
            "prohibited_decisions": [
                "recommend actions",
                "authorize maneuvers",
                "interpret facts",
                "predict the future",
                "issue commands",
                "determine final operational response",
            ],
        }
