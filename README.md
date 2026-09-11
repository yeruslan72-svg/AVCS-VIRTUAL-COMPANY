# AVCS VIRTUAL COMPANY

### Reference Implementation of the AVCS Decision Architecture

**Version:** 0.5.2 — Constitution-Aligned Sequential
**Status:** Active Development — Reference Implementation
**Project:** AVCS — Adaptive Vector Control System

---

## What This Is

**AVCS VIRTUAL COMPANY** is a working reference implementation of the AVCS decision architecture.

It is not a demonstration. It is not a prototype for show.

It is a **constitutionally-aligned system** that has been tested against its own governing principles — and passed.

The Virtual Company models how a high-risk organization can:

- receive information,
- normalize semantic meaning,
- distribute analytical responsibility across seven functional departments,
- evaluate operational conditions,
- detect structural conflicts,
- formulate decision proposals,
- control authority boundaries,
- execute approved actions,
- preserve auditable decision records.

It operates **sequentially**, not in parallel. Each department receives the structural state accumulated from previous departments. CAPTAIN is executed last, with full access to all results.

---

## AVCS as a Discipline

AVCS is not only a machine. It is a **discipline** — a structural integrity system for decisions under pressure.

The full AVCS documentation is in [`docs/`](docs/).

**Start here:** [**System Navigator**](docs/System_Navigator.md) — the map of the entire AVCS discipline.

The System Navigator shows:

- how documents relate to one another,
- in what order they should be read,
- which document governs in which domain.

### Core Documents

| Document | Role |
|---|---|
| [**Charter**](docs/Charter.md) | Constitution — North of AVCS |
| [**CORE**](docs/CORE.md) | 23 Laws of Structural Integrity |
| [**Spirit Doctrine**](docs/Spirit_Doctrine.md) | Ethical and human-sovereignty foundation |
| [**Code of Ethics**](docs/Code_of_Ethics.md) | Professional conduct |
| [**Code of Practice**](docs/Code_of_Practice.md) | Technical standard for SIM audits |
| [**Leadership Doctrine**](docs/Leadership_Doctrine.md) | Leadership principles |
| [**Leadership Code**](docs/Leadership_Code.md) | Leadership behavior |
| [**Manifest**](docs/Manifest.md) | Public identity |
| [**Strategic Narrative**](docs/Strategic_Narrative.md) | Public positioning |

### Operational Modules

| Document | Role |
|---|---|
| [**SIM**](docs/SIM.md) | Structural Integrity Module — diagnostic instrument |
| [**INS**](docs/INS.md) | Intelligence Navigation System |
| [**HPSM**](docs/HPSM.md) | Human Performance Stability Model |
| [**Execution Playbook**](docs/Execution_Playbook.md) | Operational enforcement standard |
| [**Field Guide**](docs/Field_Guide.md) | Practical handbook for Practitioners |

### Governance & Compliance

| Document | Role |
|---|---|
| [**Practitioner Council Charter**](docs/Practitioner_Council_Charter.md) | Institutional governance |
| [**Architecture Reconciliation**](docs/Architecture_Reconciliation.md) | Constitutional compliance test |

### Virtual Company Internals

| Document | Role |
|---|---|
| [**Decision Model**](docs/DECISION_MODEL.md) | Internal decision model |
| [**Department Contracts**](docs/DEPARTMENT_CONTRACTS.md) | Department responsibility boundaries |
| [**INS Architecture**](docs/INS_ARCHITECTURE.md) | Navigation architecture |

---

## Architecture

```text
INCIDENT
    │
    ▼
SEMANTIC EVENT NORMALIZER
    │
    ▼
SEQUENTIAL EXECUTOR
    │
    ├──► LOOKOUT      (foresight / signals)
    ├──► CHARTS       (structured reality)
    ├──► GYRO         (stability under pressure)
    ├──► NAVIGATOR    (strategy / direction)
    ├──► COMPASS      (North integrity / boundary authority)
    ├──► HELM         (decision authority)
    └──► CAPTAIN      (system integration / review)
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

Quick Start
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

Test Scenario
The reference test is a collision incident:

text
Collision with fishing vessel. A fishing vessel struck the port side
of the cargo ship in the engine room area. Deep dent detected, water
ingress suspected. No injuries. The vessel can continue its voyage.
Position 35°N 45°W. The weather is calm.
Expected output:

Component	Expected
Semantic Normalizer	COLLISION → ACTIVE; HULL_BREACH → UNCERTAIN; FLOODING → UNCERTAIN
LOOKOUT	signal_state: SIGNAL_DETECTED
CHARTS	reality_status: STRUCTURED
GYRO	stability_status: STABLE
NAVIGATOR	course_state: MAINTAIN
COMPASS	north_status: WITHIN NORTH, veto: false
HELM	decision_state: DECISION_MADE
CAPTAIN	structural_coherence: INTACT
Authority Gate	authority_status: AWAITING_AUTHORITY
Record	decision cycle COMPLETED; authorization state recorded as AUTHORIZED
Constitution-Aligned
The Virtual Company is constitutionally aligned.

Its architecture conforms to the AVCS Charter v1.1 and CORE v2.1.

In September 2026, the Virtual Company was tested against its own governing documents. Four recorded areas of structural divergence were detected between implementation and Constitution. The Constitution remained unchanged. The implementation was reconciled.

This is the first constitutional compliance test of AVCS on itself.

Full record: Architecture Reconciliation.

Self-Application
AVCS is subject to the same structural integrity principles it imposes on systems it evaluates.

This is not a claim. It is a structural property of the discipline.

The Virtual Company does not merely demonstrate AVCS.

It is the subject of AVCS structural integrity testing.

The drift detected during development is not an unpleasant project error. It is the first real experiment of AVCS on itself.

Core Principles
Six immovable human truths from the Spirit Doctrine:

Humans carry responsibility — not machines.

Clarity beats complexity — always.

Trust is engineered — not requested.

Safety is intentional — not accidental.

Decision power belongs to disciplined minds — not automated systems.

Evidence precedes status — not the reverse.

Five navigation principles from INS:

North is not interpreted. North is applied.

Recommendation is not authority.

Analysis is not authorization.

Capability is not permission.

Evidence precedes status.

The central diagnostic question of AVCS:

Show me the condition behind the status.

Repository Structure
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
│   ├── departments/
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
│   ├── aggregation/
│   ├── conflict_detection/
│   ├── decision_engine/
│   ├── authority_gate/
│   └── state_machine/
│
├── records/
│   └── incident_registry.py
│
├── docs/                              ← AVCS documentation (20 documents)
│   ├── System_Navigator.md            ← Start here
│   ├── Charter.md
│   ├── CORE.md
│   ├── Spirit_Doctrine.md
│   ├── Code_of_Ethics.md
│   ├── Code_of_Practice.md
│   ├── Leadership_Doctrine.md
│   ├── Leadership_Code.md
│   ├── Manifest.md
│   ├── Strategic_Narrative.md
│   ├── SIM.md
│   ├── INS.md
│   ├── HPSM.md
│   ├── Execution_Playbook.md
│   ├── Field_Guide.md
│   ├── Practitioner_Council_Charter.md
│   ├── Architecture_Reconciliation.md
│   ├── DECISION_MODEL.md
│   ├── DEPARTMENT_CONTRACTS.md
│   └── INS_ARCHITECTURE.md
│
└── tests/
Status
Current Version
v0.5.2 — Constitution-Aligned Sequential

Implemented
Semantic Event Normalizer (v0.3.9)

7 functional departments (INS-A contracts)

SequentialExecutor (Constitution-aligned order)

Structural Conflict Detector

Aggregator with risk assessment

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

Contact
Yeruslan Chihachyov
Decision Architect for High-Risk Operations
Founder — AVCS DNA MATRIX SPIRIT

LinkedIn: linkedin.com/in/yeruslan-chihachyov-70a807126

Email: yeruslan72@gmail.com

AVCS — Adaptive Vector Control System
Structural Integrity for Decisions Under Pressure

From information to decision.
From decision to controlled action.
From action to verifiable record.
