# AVCS VIRTUAL COMPANY

### Constitution-Aligned Sequential Decision Architecture

**Version:** 0.5.2 — Constitution-Aligned Sequential
**Status:** Active Development — Reference Implementation
**Project:** AVCS — Adaptive Vector Control System

---

## 1. Overview

**AVCS VIRTUAL COMPANY** is an operational simulation of the AVCS decision architecture. It models how a high-risk organization can receive information, distribute analytical responsibility across functional departments, evaluate operational conditions, formulate decision proposals, control authority boundaries, execute approved actions, and preserve auditable decision records.

The system is designed for environments where decisions must remain:

* structured,
* traceable,
* authority-controlled,
* operationally executable,
* conflict-aware,
* and reviewable after the event.

The Virtual Company is not a collection of independent AI agents.

It is a **functional organization** in which each Department (Dpt.) operates within a defined responsibility and authority boundary — and in which the execution sequence itself is Constitution-aligned.

---

## 2. Core Principle

> **AI may analyze.
> AI may recommend.
> Authority must remain explicit.
> Execution must be controlled.
> The decision pathway must remain visible.**

This principle is non-negotiable. It governs every component of the Virtual Company.

---

## 3. Architecture

The current execution model is **sequential**, not parallel.

```text
INCIDENT
   │
   ▼
SEMANTIC EVENT NORMALIZER
   │
   ▼
SEQUENTIAL EXECUTOR
   │
   ├──► LOOKOUT Dpt.     (foresight / signals)
   ├──► CHARTS Dpt.      (structured reality)
   ├──► GYRO Dpt.        (stability under pressure)
   ├──► NAVIGATOR Dpt.   (strategy / direction)
   ├──► COMPASS Dpt.     (North integrity / boundary authority)
   ├──► HELM Dpt.        (decision authority)
   └──► CAPTAIN Dpt.     (system integration / review)
   │
   ▼
AGGREGATION
   │
   ▼
STRUCTURAL CONFLICT DETECTION
   │
   ▼
DECISION PROPOSAL
   │
   ▼
AUTHORITY GATE
   │
   ▼
HUMAN AUTHORITY
   │
   ▼
EXECUTION
   │
   ▼
AVCS DECISION RECORD
The architecture separates:

information → semantic normalization → sequential assessment → aggregation → conflict detection → decision proposal → authority → execution → record

This separation is fundamental.

4. Semantic Event Normalizer
Before any department processes an incident, the Semantic Event Normalizer classifies the incoming text.

It distinguishes between:

ACTIVE — a condition is currently true

UNCERTAIN — a condition is suspected, possible, or probable

REPORTED — a condition has been reported but not confirmed

CONFIRMED — a condition has been explicitly confirmed

HISTORICAL — a condition belongs to a previous period

NEGATIVE — a condition has been explicitly ruled out

Each condition carries:

severity (CRITICAL / HIGH / MEDIUM / LOW)

semantic state

confidence score

polarity

temporal context

source

Example:

text
"Water ingress suspected"  → UNCERTAIN (confidence 0.60)
"Collision with vessel"    → ACTIVE    (confidence 0.80)
"No injuries"              → NEGATIVE  (excluded from active conditions)
This layer prevents the system from confusing the presence of a word with the presence of a condition.

5. The Seven Departments (INS-A)
Each department operates under a defined contract with explicit authority boundaries.

LOOKOUT Dpt. — Foresight & Anticipation
Detects weak signals, trends, and early deviation indicators.

Question: What is changing?

Authority: SIGNAL_AUTHORITY

Prohibited: authorize, execute, determine final threat, suppress signals.

CHARTS Dpt. — Structured Reality
Establishes facts, observations, assumptions, unknowns, contradictions.

Question: What do we actually know?

Authority: FACT_AUTHORITY

Prohibited: recommend actions, interpret facts, predict the future.

GYRO Dpt. — Stability Under Pressure
Assesses human condition, system condition, and operational load.

Question: Is the environment stable enough to act?

Authority: STABILITY_ASSESSMENT_AUTHORITY

Prohibited: recommend operational actions, authorize maneuvers.

NAVIGATOR Dpt. — Strategy & Direction
Proposes strategic course and anticipates change.

Question: Where should we go?

Authority: STRATEGIC_PROPOSAL_AUTHORITY

Prohibited: authorize action, execute, assess final threat.

COMPASS Dpt. — North Integrity / Boundary Authority
Determines whether a proposed decision remains within North.

Question: Does this decision remain within North?

Authority: BOUNDARY_AUTHORITY (veto on violation of North)

Permitted outputs: WITHIN NORTH / OUTSIDE NORTH / UNDETERMINED

Prohibited: recommend actions, calculate trajectories, execute, interpret North.

North is not interpreted. North is applied.

HELM Dpt. — Decision Authority
Makes legitimate, bounded, structurally supported decisions.

Question: What decision should be made?

Authority: DECISION_AUTHORITY (within North)

Permitted outputs: DECISION_MADE / NO_DECISION / DEFERRED / ESCALATED

Prohibited: execute, issue commands, authorize own decision.

CAPTAIN Dpt. — System Integration & Review
Reviews whether the system remained structurally coherent.

Question: Did the system remain structurally coherent?

Authority: REVIEW_AUTHORITY

Permitted outputs: INTACT / CONDITIONALLY INTACT / FRAGMENTED / BROKEN

Prohibited: authorize, execute, replace human authority.

A captain does not steer the ship. A captain ensures the ship remains a ship.

6. Sequential Execution
The Virtual Company executes departments sequentially, not in parallel.

Why sequential?

Because departments are functionally dependent:

COMPASS requires the strategic intent from NAVIGATOR.

HELM requires the North status from COMPASS, stability from GYRO, and reality from CHARTS.

CAPTAIN requires the complete results from all six previous departments.

Order:

text
1. LOOKOUT   → signal_state, trajectory
2. CHARTS    → reality_status, facts
3. GYRO      → stability_status, load_level
4. NAVIGATOR → course, course_state
5. COMPASS   → north_status, veto
6. HELM      → decision, decision_state
7. CAPTAIN   → structural_coherence, role_integrity
CAPTAIN is executed last, with full access to department_results. It reviews the system, not the decision.

7. Authority Boundary
The Authority Gate establishes the boundary between:

what the system recommends

and

what the organization authorizes.

text
DECISION PROPOSAL
       │
       ▼
AUTHORITY GATE
       │
       ▼
HUMAN AUTHORITY
The system distinguishes between:

information,

analysis,

recommendation,

authorization,

command,

execution,

result.

Critical rule: Authorization may not override North.

If COMPASS returns OUTSIDE NORTH or veto: true, the Authority Gate returns NORTH_VIOLATION — and no human authorization can proceed.

North is not negotiable.

8. Structural Conflict Detection
Operational systems cannot assume that all departments will agree.

Conflict is treated as a structural condition — not an error to be hidden.

The Structural Conflict Detector identifies conflicts between structural fields, not text:

North veto vs decision made

Unstable environment vs decision made

Contradictory reality vs decision made

Course proposed vs outside North

Deviation indicated vs intact coherence

North integrity vs North status

Role integrity broken

Conflicts are preserved in the decision record. They are never silently removed during aggregation.

9. Decision Proposal
The Decision Engine converts the aggregated operational state into a structured Decision Proposal.

A proposal contains:

operational state (assessments from all departments)

structural fields (north_status, stability_status, reality_status)

evidence

risks

recommendations

available options

constraints

conflicts

authority requirement

proposed action

status

The Decision Proposal is not equivalent to authorization.

10. AVCS Decision Record
Every completed decision cycle produces a structured AVCS record.

The record preserves the full decision pathway — not merely the final state.

text
Event ID
Timestamp
Incoming Information
Semantic Normalization
Department Assessments (7)
Aggregated State
Structural Fields
Conflict Result
Decision Proposal
Authority State
Authorization
Decision Record (final)
Critical property: one event_id per cycle. Every department, every aggregation, every decision, every record — same ID.

This makes the decision externally reviewable.

11. Drift Detection (Self-Applied)
AVCS was designed to detect drift — the silent normalization of small deviations.

During development of the Virtual Company, AVCS applied this principle to itself.

Four structural drifts were detected and resolved:

Drift	Description	Resolution
001	Implementation redefined the meaning of departmental roles (INS-B vs INS-A)	Roles restored to Constitution
002	Implementation assumed a parallel execution model while Constitution required sequential	SequentialExecutor introduced
003	Conflict detection checked text, not structure	Structural Conflict Detector implemented
004	Sequential dependency incomplete (COMPASS, CAPTAIN not receiving accumulated state)	Order of execution corrected
Two principles were established:

Code must implement the Constitution — not redefine it.

If implementation and Constitution diverge, the divergence becomes a test result — not an automatic Constitutional change.

The Constitution was not modified. The implementation was reconciled.

This is not a failure. This is validation.

12. Test Scenario
The current reference test is a collision incident.

Input:

text
Collision with fishing vessel. A fishing vessel struck the port side
of the cargo ship in the engine room area. Deep dent detected, water
ingress suspected. No injuries. The vessel can continue its voyage.
Position 35°N 45°W. The weather is calm.
Object: Cargo ship
Position: 35°N 45°W

Expected output:

text
Semantic Normalizer:
  COLLISION      → ACTIVE    (0.80)
  HULL_BREACH    → UNCERTAIN (0.60)
  FLOODING       → UNCERTAIN (0.60)

Departments (INS-A):
  LOOKOUT    → SIGNAL_DETECTED
  CHARTS     → STRUCTURED
  GYRO       → STABLE
  NAVIGATOR  → MAINTAIN
  COMPASS    → WITHIN NORTH (veto: false)
  HELM       → DECISION_MADE (CONTINUE)
  CAPTAIN    → INTACT (6 departments reviewed)

Structural Fields:
  North:     WITHIN NORTH
  Veto:      NO
  Stability: STABLE
  Reality:   STRUCTURED
  Coherence: INTACT
  Decision:  DECISION_MADE

Authority Gate:
  authority_status: AWAITING_AUTHORITY

After human approval:
  status: AUTHORIZED
13. Repository Structure
text
AVCS-VIRTUAL-COMPANY/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── app/
│   ├── streamlit_app.py
│   ├── logo.png
│   └── north_is_not_negotiable.png
│
├── core/
│   ├── __init__.py
│   │
│   ├── departments/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── lookout.py
│   │   ├── charts.py
│   │   ├── gyro.py
│   │   ├── navigator.py
│   │   ├── compass.py
│   │   ├── helm.py
│   │   └── captain.py
│   │
│   ├── sequential_executor/
│   │   ├── __init__.py
│   │   └── sequential_executor.py
│   │
│   ├── aggregation/
│   │   ├── __init__.py
│   │   └── aggregator.py
│   │
│   ├── conflict_detection/
│   │   ├── __init__.py
│   │   └── conflict_detector.py
│   │
│   ├── decision_engine/
│   │   ├── __init__.py
│   │   └── decision_engine.py
│   │
│   ├── authority_gate/
│   │   ├── __init__.py
│   │   └── authority_gate.py
│   │
│   ├── state_machine/
│   │   ├── __init__.py
│   │   └── state_machine.py
│   │
│   ├── dispatcher/
│   │   └── dispatcher.py    (legacy — not used in execution path)
│   │
│   ├── event_normalizer/
│   ├── risk_engine/
│   └── semantic_analyzer/
│
├── records/
│   ├── __init__.py
│   └── incident_registry.py
│
├── tests/
│
└── docs/
14. Quick Start
Requirements:

Python 3.10+

Streamlit

Standard scientific stack (pandas, plotly, etc.)

Install:

bash
git clone https://github.com/yeruslan72-svg/AVCS-VIRTUAL-COMPANY.git
cd AVCS-VIRTUAL-COMPANY
pip install -r requirements.txt
Run:

bash
streamlit run app/streamlit_app.py
Open the browser at http://localhost:8501.

15. Development Status
Current Version
v0.5.2 — Constitution-Aligned Sequential

Implemented
Semantic Event Normalizer (v0.3.9)

7 functional departments (INS-A contracts)

SequentialExecutor (Constitution-aligned order)

Structural Conflict Detector

Aggregator with risk_assessment

Decision Engine

Authority Gate with North veto protection

State Machine (tracker)

Incident Registry

Streamlit UI (5 tabs)

Not Yet Implemented
Real LLM-based analytical components (currently rule-based)

Production-grade orchestration

Cryptographic authentication

Immutable external verification

Real-time industrial integration

Multi-scenario library

Non-intervention case (Case L)

These are future development stages.

16. Relationship to AVCS
AVCS VIRTUAL COMPANY is a reference implementation for testing AVCS structural concepts.

The Virtual Company allows AVCS principles to be examined through executable operational scenarios — not documentation alone.

The project is concerned with the transition:

text
REQUIREMENT
     ↓
OPERATIONAL CONDITION
     ↓
DECISION
     ↓
AUTHORITY
     ↓
ACTION
     ↓
VERIFIABLE RECORD
The critical question is not only:

Can an AI system recommend an action?

The more important question is:

Can the organizational architecture ensure that a critical requirement is converted into a controlled, authorized, executable, and reviewable operational action?

17. Future Research Boundary
The first implementation focuses on a completed intervention pathway.

A more difficult structural problem will subsequently be tested:

text
A critical condition is detected.
An intervention is possible.
The operator decides NOT to intervene.
The operation continues.
Later, an external reviewer asks:

  Was the non-intervention legitimate?
  Can that legitimacy be demonstrated?
  Can the state of non-action be externally verified?
This is the Non-Intervention Decision Boundary (Case L).

It represents a separate research boundary within AVCS. The positive-control implementation must precede the non-intervention case.

18. Project Principle
AI may analyze.
AI may recommend.
Authority must remain explicit.
Execution must be controlled.
The decision pathway must remain visible.

19. Contact
Yeruslan Chihachyov
Decision Architect for High-Risk Operations
Founder — AVCS DNA MATRIX SPIRIT

LinkedIn: linkedin.com/in/yeruslan-chihachyov-70a807126

Email: yeruslan72@gmail.com

AVCS VIRTUAL COMPANY
Adaptive Vector Control System

From information to decision.
From decision to controlled action.
From action to verifiable record.
