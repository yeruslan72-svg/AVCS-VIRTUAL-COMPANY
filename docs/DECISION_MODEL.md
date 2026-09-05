# Decision Model

## Core Principle

AI may analyze. AI may recommend. Authority must remain explicit. Execution must be controlled. The decision pathway must remain visible.

## Decision States

| State | Description |
|-------|-------------|
| IDLE | System ready |
| EVENT_RECEIVED | Event received |
| DISPATCHING | Routing to departments |
| DEPARTMENTS_PROCESSING | Departments processing |
| AGGREGATING | Consolidating results |
| CONFLICT_DETECTING | Detecting conflicts |
| DECISION_FORMULATING | Formulating decision |
| AWAITING_AUTHORITY | Waiting for human approval |
| AUTHORIZED | Decision authorized |
| REJECTED | Decision rejected |
| EXECUTING | Executing action |
| COMPLETED | Decision cycle complete |

## Authority Boundary

AI ANALYSIS → AI RECOMMENDATION → (AUTHORITY BOUNDARY) → HUMAN AUTHORITY → AUTHORIZED COMMAND → EXECUTION

## Decision Record

Every completed decision cycle produces an AVCS Record containing:
- Event ID
- Decision ID
- Department assessments
- Evidence
- Conflicts
- Decision proposal
- Authorization status
- Execution result
- Timestamps
