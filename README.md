# AVCS VIRTUAL COMPANY

### AI-Driven Functional Operational Decision Architecture

**Version:** 0.1 — Functional Organization Prototype
**Status:** Active Development
**Project:** AVCS — Adaptive Vector Control System

---

## 1. Overview

**AVCS VIRTUAL COMPANY** is an AI-driven functional operational architecture designed to model how complex organizations can receive information, distribute analytical responsibilities, evaluate operational conditions, formulate decision proposals, control authority boundaries, execute approved actions, and maintain auditable decision records.

The system is designed for environments where decisions must remain:

* structured,
* traceable,
* authority-controlled,
* operationally executable,
* conflict-aware,
* and auditable after the event.

The Virtual Company is not designed as a collection of independent AI chatbots.

It is designed as a **functional organization** in which each Department (Dpt.) operates within a defined responsibility and authority boundary.

---

# 2. Core Concept

The fundamental AVCS VIRTUAL COMPANY execution model is:

```text
INCOMING INFORMATION
        │
        ▼
┌───────────────────┐
│   AI DISPATCHER   │
└─────────┬─────────┘
          │
          ▼
┌───────────────────────────────────────────────┐
│              FUNCTIONAL Dpts.                 │
│                                               │
│ LOOKOUT │ CHARTS │ GYRO │ NAVIGATOR          │
│ COMPASS │ HELM   │ CAPTAIN                    │
└──────────────────────┬────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │   AGGREGATION  │
              └───────┬────────┘
                      │
                      ▼
             DECISION PROPOSAL
                      │
                      │
              AUTHORITY BOUNDARY
                      │
                      ▼
             HUMAN AUTHORITY
                      │
                      ▼
                 EXECUTION
                      │
                      ▼
                AVCS RECORD
```

The architecture separates:

**information → analysis → aggregation → decision proposal → authority → execution → record**

This separation is fundamental to the system.

---

# 3. Functional Departments

The Virtual Company consists of seven functional departments.

The term **Dpt.** explicitly identifies these as functional organizational units within the Virtual Company.

They are not intended to represent literal shipboard job positions.

---

## LOOKOUT Dpt.

### Primary Function

Detection and observation.

### Responsibilities

* detect relevant operational information;
* identify anomalies and emerging conditions;
* establish initial observations;
* report observable facts;
* maintain observation timestamps.

### Boundary

LOOKOUT Dpt. may identify and report a condition.

It does not independently determine the final operational response.

---

## CHARTS Dpt.

### Primary Function

Contextual and environmental assessment.

### Responsibilities

* evaluate geographic/contextual information;
* identify restricted or controlled areas;
* assess relevant operational constraints;
* correlate observations with known environmental information;
* identify contextual hazards.

### Boundary

CHARTS Dpt. provides contextual information and assessment.

It does not hold final decision authority.

---

## GYRO Dpt.

### Primary Function

Motion and tracking assessment.

### Responsibilities

* establish movement characteristics;
* evaluate heading and track;
* monitor changes in motion;
* verify trajectory information;
* identify deviations from expected movement.

### Boundary

GYRO Dpt. provides motion-related evidence.

It does not independently authorize operational action.

---

## NAVIGATOR Dpt.

### Primary Function

Threat and situation assessment.

### Responsibilities

* integrate relevant operational information;
* assess projected consequences;
* evaluate threat conditions;
* determine whether intervention may be required;
* provide an operational recommendation.

### Boundary

NAVIGATOR Dpt. may recommend an action.

It does not possess final authority to execute that action.

---

## COMPASS Dpt.

### Primary Function

Action and trajectory recommendation.

### Responsibilities

* evaluate possible operational responses;
* calculate or recommend an appropriate course/action;
* assess separation or trajectory consequences;
* provide a specific operational recommendation.

### Boundary

COMPASS Dpt. recommends an action.

It does not independently authorize execution.

---

## HELM Dpt.

### Primary Function

Execution readiness and execution control.

### Responsibilities

* evaluate whether the proposed action can be executed;
* verify operational readiness;
* identify execution constraints;
* execute an authorized command;
* report execution status;
* confirm resulting operational state.

### Boundary

HELM Dpt. does not independently create final authority.

Execution requires an authorized command.

---

## CAPTAIN Dpt.

### Primary Function

Decision authority interface.

CAPTAIN Dpt. represents the highest functional authority layer within the Virtual Company architecture.

### Responsibilities

* receive the aggregated decision state;
* review evidence and recommendations;
* identify unresolved conflicts;
* present the decision state to human authority;
* receive authorization;
* issue or transmit an authorized command;
* maintain the decision record;
* initiate stand-down or continuation when authorized.

### Critical Boundary

CAPTAIN Dpt. is **not intended to replace human authority**.

The architecture maintains an explicit authority boundary:

```text
AI ANALYSIS
     ↓
DECISION PROPOSAL
     ↓
AUTHORITY GATE
     ↓
HUMAN AUTHORITY
     ↓
AUTHORIZED ACTION
```

The purpose of this boundary is to prevent analytical capability from being confused with operational authority.

---

# 4. AI Dispatcher

The **AI Dispatcher** is the information-routing layer of the Virtual Company.

Its primary function is to determine:

> Which functional Dpts. need to receive and process a particular incoming event?

The Dispatcher does not make the final operational decision.

Example:

```text
Incoming Event
      │
      ▼
AI Dispatcher
      │
      ├──► LOOKOUT Dpt.
      ├──► CHARTS Dpt.
      ├──► GYRO Dpt.
      ├──► NAVIGATOR Dpt.
      ├──► COMPASS Dpt.
      ├──► HELM Dpt.
      └──► CAPTAIN Dpt.
```

Routing may be dynamic.

Not every event necessarily requires every Dpt.

The Dispatcher therefore acts as an **organizational information router**, not as the final decision-maker.

---

# 5. Department Contracts

Each functional Dpt. operates under a defined contract.

A Department Contract establishes:

```text
PURPOSE
INPUT
PROCESSING RESPONSIBILITY
OUTPUT
AUTHORITY
MANDATORY ACTIONS
PERMITTED RECOMMENDATIONS
PROHIBITED DECISIONS
```

Conceptually:

```text
┌──────────────────────────────┐
│       DEPARTMENT CONTRACT    │
├──────────────────────────────┤
│ Purpose                      │
│ Inputs                       │
│ Responsibilities             │
│ Outputs                      │
│ Authority Boundary           │
│ Required Actions             │
│ Permitted Recommendations    │
│ Prohibited Decisions         │
└──────────────────────────────┘
```

These contracts are intended to prevent functional overlap and uncontrolled authority propagation between AI components.

---

# 6. Aggregation

The Aggregation layer receives outputs from relevant functional Dpts.

Its purpose is to construct a consolidated operational state.

Example:

```text
LOOKOUT ───────┐
CHARTS ────────┤
GYRO ──────────┤
NAVIGATOR ─────┤
COMPASS ───────┤──► AGGREGATION
HELM ──────────┤
CAPTAIN ───────┘
```

The Aggregator does not simply select the answer of one Department.

It must preserve:

* supporting evidence;
* conflicting assessments;
* recommendations;
* uncertainty;
* timestamps;
* Department identity;
* decision dependencies.

---

# 7. Conflict Detection

Operational systems cannot assume that all functional units will agree.

Therefore, disagreement is treated as a structural condition rather than an error to be hidden.

Example:

```text
NAVIGATOR Dpt.
"Intervention Required"

        VS.

HELM Dpt.
"Action Cannot Be Executed"
```

The system should produce:

```text
CONFLICT DETECTED

Decision execution blocked.

CAPTAIN REVIEW REQUIRED.
```

A conflict must remain visible in the operational record.

It must not be silently removed during aggregation.

---

# 8. Decision State

The Decision Engine converts the aggregated operational state into a structured **Decision Proposal**.

A decision proposal should identify:

* current operational state;
* relevant evidence;
* detected risks;
* recommendations;
* available actions;
* constraints;
* conflicts;
* authority requirement;
* proposed action;
* required execution conditions.

Conceptually:

```text
OPERATIONAL STATE
       ↓
EVIDENCE
       ↓
ASSESSMENT
       ↓
RECOMMENDATIONS
       ↓
CONFLICT CHECK
       ↓
DECISION PROPOSAL
```

The Decision Proposal is not equivalent to authorization.

---

# 9. Authority Gate

The Authority Gate establishes the boundary between:

**what the system recommends**

and

**what the organization authorizes**.

```text
DECISION PROPOSAL
       │
       ▼
┌──────────────────┐
│  AUTHORITY GATE  │
└────────┬─────────┘
         │
         ▼
 HUMAN AUTHORITY
```

The system must be able to distinguish between:

* information;
* analysis;
* recommendation;
* authorization;
* command;
* execution;
* result.

This distinction is central to AVCS structural integrity.

---

# 10. Execution

Once an action is authorized, the execution pathway becomes explicit.

Example:

```text
RECOMMENDATION
      ↓
AUTHORIZATION
      ↓
COMMAND
      ↓
HELM Dpt.
      ↓
EXECUTION
      ↓
EXECUTION CONFIRMATION
      ↓
RESULT
```

The system must preserve the relationship between the authorized decision and the resulting operational action.

---

# 11. AVCS Decision Record

Every completed decision cycle should produce a structured AVCS record.

The record is intended to make the operational pathway reviewable after the event.

A future AVCS record may contain:

```text
Event ID
Decision ID
Scenario ID

Incoming Information
Dispatcher Routing
Department Assessments
Department Recommendations
Aggregation State
Detected Conflicts
Decision Proposal
Authority State
Authorization
Command
Execution
Execution Confirmation
Operational Result
Stand-Down / Continuation
Timestamps
Integrity Metadata
```

The objective is not merely to create a log.

The objective is to preserve the **decision pathway**.

---

# 12. Operational Decision Chain

The initial positive-control scenario follows this sequence:

```text
DETECTION
    ↓
ASSESSMENT
    ↓
THREAT DETERMINATION
    ↓
RECOMMENDATION
    ↓
AUTHORITY
    ↓
EXECUTION
    ↓
CONFIRMATION
    ↓
RESULT
    ↓
STAND-DOWN
```

This sequence represents the first operational pathway to be implemented in the Virtual Company.

---

# 13. Initial Test Scenario — Drone

The first integrated scenario is an unidentified drone detected near a protected operational environment.

The scenario is used as a controlled test of the Virtual Company architecture.

The operational sequence is:

```text
LOOKOUT
   ↓
CHARTS
   ↓
GYRO
   ↓
NAVIGATOR
   ↓
COMPASS
   ↓
HELM
   ↓
CAPTAIN
```

The scenario tests whether the system can:

1. receive an incoming event;
2. distribute information;
3. perform functional assessments;
4. aggregate the assessments;
5. identify potential conflicts;
6. formulate a decision proposal;
7. pass through an authority boundary;
8. obtain human authorization;
9. execute the authorized action;
10. confirm the resulting state;
11. generate an auditable AVCS record.

---

# 14. Structural Objective

The primary objective of AVCS VIRTUAL COMPANY is not to create increasingly autonomous AI agents.

The objective is to demonstrate that AI capability can operate inside a controlled organizational structure.

The architecture therefore prioritizes:

### Separation of Function

Different Dpts. perform different functions.

### Separation of Authority

Analytical capability does not automatically create authority.

### Traceability

Decision-relevant information remains connected to the resulting action.

### Conflict Visibility

Disagreement is preserved rather than silently suppressed.

### Controlled Execution

An action becomes executable only through an explicit authority pathway.

### Auditability

The system preserves the sequence required to reconstruct how a decision moved from information to action.

---

# 15. Development Philosophy

Development will proceed from **structure to execution**.

The project will not begin by building a complex user interface or a collection of unrestricted AI agents.

The intended development sequence is:

```text
1. FUNCTIONAL ARCHITECTURE
          ↓
2. DEPARTMENT CONTRACTS
          ↓
3. AI DISPATCHER
          ↓
4. DEPARTMENT PROCESSING
          ↓
5. AGGREGATION
          ↓
6. CONFLICT DETECTION
          ↓
7. DECISION ENGINE
          ↓
8. AUTHORITY GATE
          ↓
9. EXECUTION SIMULATION
          ↓
10. AVCS RECORD
          ↓
11. OPERATIONAL UI
```

---

# 16. Planned Repository Structure

The target repository architecture is:

```text
AVCS-VIRTUAL-COMPANY/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── app/
│   ├── streamlit_app.py
│   └── ui/
│
├── core/
│   ├── dispatcher/
│   │
│   ├── departments/
│   │   ├── lookout.py
│   │   ├── charts.py
│   │   ├── gyro.py
│   │   ├── navigator.py
│   │   ├── compass.py
│   │   ├── helm.py
│   │   └── captain.py
│   │
│   ├── aggregation/
│   ├── decision_engine/
│   ├── authority_gate/
│   ├── conflict_detection/
│   └── state_machine/
│
├── records/
│   ├── avcs_record.py
│   └── schemas/
│
├── scenarios/
│   └── drone/
│
├── simulation/
│
├── tests/
│
├── config/
│
└── docs/
    ├── INS_ARCHITECTURE.md
    ├── DEPARTMENT_CONTRACTS.md
    └── DECISION_MODEL.md
```

This structure will evolve as the architecture is tested.

---

# 17. Technology Direction

The initial implementation is expected to use:

* Python
* Streamlit
* structured JSON contracts
* LLM-based analytical components
* rule-based authority controls
* state-machine logic
* simulation environments
* structured AVCS records

Future integration may include:

* OPC-UA
* Modbus
* MQTT
* REST APIs
* SCADA interfaces
* industrial controllers
* live sensor streams

The initial development environment remains **simulation-first**.

No direct control of real industrial equipment is required for the prototype.

---

# 18. Development Status

### Current Version

**v0.1 — Functional Organization Prototype**

### Current Focus

* repository architecture;
* functional Department definition;
* Department Contracts;
* AI Dispatcher;
* Drone Scenario;
* decision-state architecture;
* authority boundary;
* AVCS record structure.

### Not Yet Implemented

* production-grade LLM orchestration;
* real-time industrial integration;
* cryptographic authentication;
* immutable external verification;
* production deployment;
* autonomous control of physical systems.

These are future development stages.

---

# 19. Relationship to AVCS

AVCS VIRTUAL COMPANY is an implementation environment for testing AVCS structural concepts.

The Virtual Company allows AVCS principles to be examined through executable operational scenarios rather than documentation alone.

The project is particularly concerned with the transition:

```text
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
```

The critical question is not only:

> Can an AI system recommend an action?

The more important question is:

> Can the organizational architecture ensure that a critical requirement is converted into a controlled, authorized, executable, and reviewable operational action?

---

# 20. Future Research Boundary

The first implementation focuses on a completed intervention pathway.

A more difficult structural problem will subsequently be tested:

```text
A critical condition is detected.

An intervention is possible.

The operator decides NOT to intervene.

The operation continues.

Later, an external reviewer asks:

Was the non-intervention legitimate?

Can that legitimacy be demonstrated?

Can the state of non-action be externally verified?
```

This represents a separate research boundary within AVCS.

The positive-control implementation must therefore precede the non-intervention case.

---

# 21. Project Principle

AVCS VIRTUAL COMPANY is built around one central principle:

> **AI may analyze.
> AI may recommend.
> Authority must remain explicit.
> Execution must be controlled.
> The decision pathway must remain visible.**

---

# 22. Project Status

**AVCS VIRTUAL COMPANY is an active research and development project.**

The initial objective is to create a functioning Virtual Company capable of processing a controlled operational scenario from incoming information through decision, human authorization, execution, result confirmation, and AVCS recording.

The architecture will be refined through implementation, simulation, testing, and controlled failure analysis.

---

**AVCS VIRTUAL COMPANY**
**Adaptive Vector Control System**

*From information to decision.
From decision to controlled action.
From action to verifiable record.*
