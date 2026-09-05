# AVCS VIRTUAL COMPANY
## FUNCTIONAL DEPARTMENT CONTRACTS

**Document:** docs/DEPARTMENT_CONTRACTS.md  
**Version:** 0.1  
**Status:** Active Development  
**Project:** AVCS — Adaptive Vector Control System  
**Architecture:** INS — Functional Operational Decision Architecture

---

## 1. Purpose

This document defines the functional contracts of the seven INS Departments.

The Departments are functional AI units within an operational decision architecture. They are not independent autonomous agents.

Each Department has:
- a defined operational purpose
- defined information inputs
- a constrained processing responsibility
- defined outputs
- explicit authority boundaries
- mandatory actions
- permitted recommendations
- prohibited decisions
- uncertainty and failure conditions

The purpose of the contracts is to ensure that analytical capability does not silently become operational authority.

---

## 2. Core Principle

The INS architecture separates:

INFORMATION
↓
ANALYSIS
↓
ASSESSMENT
↓
RECOMMENDATION
↓
AUTHORITY
↓
COMMAND
↓
EXECUTION
↓
RESULT

A Department may perform analysis and provide recommendations within its defined scope. A Department does not acquire final authority merely because its recommendation is technically strong.

---

## 3. Common Department Contract

Every Department shall conform to the following logical contract:

DEPARTMENT CONTRACT

PURPOSE:
What operational function does this Department perform?

INPUT:
What information may the Department receive?

PROCESSING RESPONSIBILITY:
What may the Department analyze?

OUTPUT:
What structured information must it produce?

AUTHORITY:
What authority does the Department possess?

MANDATORY ACTIONS:
What must the Department always do?

PERMITTED RECOMMENDATIONS:
What may the Department recommend?

PROHIBITED DECISIONS:
What must the Department never decide?

UNCERTAINTY:
How must incomplete, conflicting, or uncertain information be represented?

---

## 4. Standard Output Requirements

Each Department shall return a structured result containing, at minimum:

{
  "department": "",
  "event_id": "",
  "timestamp": "",
  "assessment": "",
  "evidence": [],
  "confidence": null,
  "uncertainty": [],
  "constraints": [],
  "recommendations": [],
  "authority_state": "NO_AUTHORITY",
  "status": ""
}

The exact implementation schema may evolve. The architectural rule remains:

Department output is evidence, assessment, or recommendation — not authorization.

---

## 5. LOOKOUT Dpt.

### PURPOSE

Detect and report observable operational events. LOOKOUT Dpt. represents the observation and detection function of the INS architecture. Its primary responsibility is to establish:

What is being observed?

### INPUT

Possible inputs include:
- sensor observations
- visual observations
- radar/tracking data
- external alerts
- system alarms
- object detections
- operator observations
- timestamps
- positional information

### PROCESSING RESPONSIBILITY

LOOKOUT Dpt. may:
- detect objects or events
- identify observable characteristics
- establish initial position
- establish bearing/range where available
- identify movement
- establish observation timestamps
- distinguish known from unknown information

### OUTPUT

LOOKOUT Dpt. shall provide:
- detected object/event
- observation time
- location/bearing/range where available
- observed movement
- identification status
- supporting evidence
- uncertainty

### AUTHORITY

AUTHORITY: NONE

LOOKOUT Dpt. cannot authorize operational action.

### MANDATORY ACTIONS

LOOKOUT Dpt. must:
- record detected events
- preserve timestamps
- distinguish observation from interpretation
- identify missing information
- report uncertainty
- forward relevant information to the HUB

### PERMITTED RECOMMENDATIONS

LOOKOUT Dpt. may recommend:
- further observation
- tracking
- information verification
- escalation of an observation for assessment

### PROHIBITED DECISIONS

LOOKOUT Dpt. must not:
- authorize maneuver
- issue operational commands
- determine final threat status
- authorize intervention
- suppress observations because they appear insignificant

---

## 6. CHARTS Dpt.

### PURPOSE

Provide environmental, geographic, spatial, and contextual constraints.

Primary question: Where is the event occurring, and what constraints apply?

### INPUT

Possible inputs include:
- charts
- geographic data
- restricted areas
- exclusion zones
- navigational constraints
- environmental restrictions
- known hazards
- operational boundaries

### PROCESSING RESPONSIBILITY

CHARTS Dpt. may:
- determine geographic context
- identify restricted or protected areas
- identify relevant boundaries
- identify known hazards
- determine applicable spatial constraints
- compare observed position against defined operational zones

### OUTPUT

CHARTS Dpt. shall provide:
- relevant geographic context
- applicable restrictions
- identified hazards
- boundary status
- spatial constraints
- supporting chart/data reference
- uncertainty

### AUTHORITY

AUTHORITY: NONE

### MANDATORY ACTIONS

CHARTS Dpt. must:
- identify applicable spatial constraints
- preserve the data reference used
- distinguish factual restrictions from interpretation
- report uncertainty
- identify conflicting spatial information

### PERMITTED RECOMMENDATIONS

CHARTS Dpt. may recommend:
- maintaining separation
- avoiding a restricted area
- additional geographic verification
- consideration of specific spatial constraints

### PROHIBITED DECISIONS

CHARTS Dpt. must not:
- authorize maneuver
- issue commands
- determine final operational response
- override another Department
- suppress geographic constraints

---

## 7. GYRO Dpt.

### PURPOSE

Establish movement, heading, tracking, trajectory, and motion-related evidence.

Primary question: How is the situation moving?

### INPUT

Possible inputs include:
- heading
- course
- speed
- bearing
- track
- rate of movement
- trajectory
- motion sensors
- historical track data

### PROCESSING RESPONSIBILITY

GYRO Dpt. may:
- establish current heading
- analyze movement
- establish trajectory
- identify changes in motion
- calculate relevant movement parameters
- detect deviations from expected movement

### OUTPUT

GYRO Dpt. shall provide:
- current heading
- track
- speed
- trajectory
- movement trend
- deviations
- timestamped motion evidence
- uncertainty

### AUTHORITY

AUTHORITY: NONE

### MANDATORY ACTIONS

GYRO Dpt. must:
- maintain temporal consistency
- identify changes in trajectory
- distinguish measured data from calculated estimates
- report degraded or unreliable data
- preserve motion evidence

### PERMITTED RECOMMENDATIONS

GYRO Dpt. may recommend:
- continued tracking
- trajectory monitoring
- verification of unexpected movement
- recalculation where data quality changes

### PROHIBITED DECISIONS

GYRO Dpt. must not:
- authorize maneuver
- issue commands
- determine final threat
- authorize intervention
- alter operational objectives

---

## 8. NAVIGATOR Dpt.

### PURPOSE

Assess the operational situation and determine potential threat, consequence, and need for intervention.

Primary question: What does the developing situation mean operationally?

### INPUT

NAVIGATOR Dpt. receives relevant outputs from:
- LOOKOUT Dpt.
- CHARTS Dpt.
- GYRO Dpt.
- other validated operational information

### PROCESSING RESPONSIBILITY

NAVIGATOR Dpt. may:
- assess the developing situation
- identify potential threats
- project consequences
- assess time-to-event
- determine whether intervention appears operationally necessary
- identify decision dependencies
- evaluate available response requirements

### OUTPUT

NAVIGATOR Dpt. shall provide:
- situation assessment
- threat assessment
- projected consequence
- time-to-event
- intervention assessment
- supporting evidence
- uncertainty
- recommendation where appropriate

### AUTHORITY

AUTHORITY: NONE

NAVIGATOR Dpt. can determine that a condition appears to require intervention. It cannot authorize that intervention.

### MANDATORY ACTIONS

NAVIGATOR Dpt. must:
- identify the basis of its assessment
- preserve supporting evidence
- identify assumptions
- identify uncertainty
- identify time sensitivity
- identify consequences of inaction where reasonably determinable
- explicitly state when available information is insufficient

### PERMITTED RECOMMENDATIONS

NAVIGATOR Dpt. may recommend:
- intervention
- continued monitoring
- additional assessment
- escalation
- consideration of specified response options

### PROHIBITED DECISIONS

NAVIGATOR Dpt. must not:
- authorize intervention
- issue execution commands
- directly control HELM
- override human authority
- represent recommendation as authorization

---

## 9. COMPASS Dpt.

### PURPOSE

Develop operational response options and calculate/recommend appropriate trajectory or action parameters.

Primary question: What response could achieve the required operational objective?

### INPUT

Possible inputs include:
- NAVIGATOR assessment
- current heading
- current speed
- trajectory
- geographic constraints
- operational restrictions
- vessel/system capabilities
- required separation
- available response options

### PROCESSING RESPONSIBILITY

COMPASS Dpt. may:
- calculate response options
- evaluate trajectories
- calculate separation
- identify feasible headings
- compare response alternatives
- recommend a specific operational response

### OUTPUT

COMPASS Dpt. shall provide:
- proposed action
- proposed heading/course/trajectory
- expected result
- safety/separation parameters
- assumptions
- constraints
- alternative options where relevant
- uncertainty

### AUTHORITY

AUTHORITY: NONE

A technically optimal recommendation does not constitute authorization.

### MANDATORY ACTIONS

COMPASS Dpt. must:
- identify calculation basis
- identify constraints
- identify assumptions
- provide expected consequences
- identify alternative options where material
- report when no feasible response is identified

### PERMITTED RECOMMENDATIONS

COMPASS Dpt. may recommend:
- heading
- course
- trajectory
- separation strategy
- speed adjustment
- alternative response options

### PROHIBITED DECISIONS

COMPASS Dpt. must not:
- authorize the response
- issue the command
- directly control HELM
- bypass CAPTAIN Dpt.
- convert recommendation into execution

---

## 10. HELM Dpt.

### PURPOSE

Determine execution readiness and perform authorized operational execution.

Primary question: Can the authorized action be executed, and what happened when it was executed?

### INPUT

Possible inputs include:
- authorized command
- proposed action
- system status
- control availability
- equipment readiness
- execution parameters

### PROCESSING RESPONSIBILITY

HELM Dpt. may:
- assess execution feasibility
- identify execution constraints
- verify system readiness
- execute an authorized command
- report execution status
- confirm execution result

### OUTPUT

HELM Dpt. shall provide:
- readiness status
- execution feasibility
- identified constraints
- command received
- execution timestamp
- execution status
- execution result
- failure state where applicable

### AUTHORITY

AUTHORITY: EXECUTION ONLY

HELM Dpt. may execute an authorized command. It does not possess independent authority to create or authorize that command.

### MANDATORY ACTIONS

HELM Dpt. must:
- verify command receipt
- verify execution readiness
- identify inability to execute
- execute only authorized commands
- record execution
- report result
- report execution failure immediately

### PERMITTED RECOMMENDATIONS

HELM Dpt. may recommend:
- execution feasibility
- alternative execution method
- delay due to technical limitation
- technical constraint requiring CAPTAIN review

### PROHIBITED DECISIONS

HELM Dpt. must not:
- create independent operational objectives
- authorize its own command
- execute an unauthorized action
- suppress execution failure
- redefine an authorized command without authority

---

## 11. CAPTAIN Dpt.

### PURPOSE

Provide the decision-authority interface between the INS decision architecture and the authorized human decision-maker.

Primary question: What decision state is presented to human authority, and what authorized action follows?

### INPUT

CAPTAIN Dpt. receives:
- aggregated Department assessments
- evidence
- recommendations
- conflicts
- constraints
- uncertainty
- proposed actions
- execution readiness
- authority requirements

### PROCESSING RESPONSIBILITY

CAPTAIN Dpt. may:
- assemble the decision state
- identify unresolved conflicts
- identify authority requirements
- present available options
- receive human authorization
- transmit authorized commands
- record the resulting authority transition
- initiate stand-down when conditions are satisfied

### OUTPUT

CAPTAIN Dpt. shall provide:
- decision state
- available options
- unresolved conflicts
- authority requirement
- human authorization status
- authorized command where applicable
- decision timestamp
- decision record reference

### AUTHORITY

AUTHORITY: HUMAN AUTHORITY INTERFACE

CAPTAIN Dpt. does not replace the human authority. The Department provides the structured interface through which the human authority: approves, rejects, modifies, withholds, or otherwise controls the decision.

### MANDATORY ACTIONS

CAPTAIN Dpt. must:
- preserve the complete decision state
- identify material conflicts
- identify missing information
- distinguish recommendation from authorization
- identify who/what holds authority
- record authorization
- record command transmission
- preserve execution confirmation
- preserve the final operational result
- prevent silent transition from recommendation to execution

### PERMITTED RECOMMENDATIONS

CAPTAIN Dpt. may present:
- recommended action
- alternative actions
- continuation
- intervention
- request for additional information
- stand-down
- escalation

### PROHIBITED DECISIONS

CAPTAIN Dpt. must not:
- silently convert an AI recommendation into authorization
- conceal unresolved conflicts
- fabricate human authorization
- represent a recommendation as a human decision
- authorize action without the required authority state

---

## 12. Cross-Department Rules

The following rules apply to every Department.

### Rule 1 — No Silent Authority
No Department may acquire authority merely through technical confidence.

### Rule 2 — Evidence Before Conclusion
Where practical, assessments shall identify the evidence on which they depend.

### Rule 3 — Uncertainty Must Remain Visible
Unknown information shall not be silently converted into certainty.

### Rule 4 — Conflicts Must Be Preserved
If two Departments produce materially incompatible assessments, the conflict shall remain visible to the Aggregation/Decision layer. It shall not be silently averaged away.

### Rule 5 — Recommendation Is Not Authorization
RECOMMENDATION ≠ AUTHORIZATION

### Rule 6 — Authorization Is Not Execution
AUTHORIZATION ≠ EXECUTION

### Rule 7 — Execution Requires Confirmation
Where execution is expected, the architecture shall distinguish:
COMMAND ISSUED → COMMAND RECEIVED → EXECUTION → RESULT

### Rule 8 — Department Identity Is Preserved
Every material output must retain the identity of the originating Department.

### Rule 9 — Timestamp Integrity
Material observations, assessments, recommendations, authorization, execution, and results shall be timestamped.

### Rule 10 — No Retroactive Reconstruction
The architecture shall preserve decision-state information at the time it existed. The system must not depend exclusively on reconstruction after the event.

---

## 13. Department Interaction Model

The normal positive-control pathway is:

LOOKOUT → CHARTS → GYRO → NAVIGATOR → COMPASS → HELM → CAPTAIN → HUMAN AUTHORITY → AUTHORIZED COMMAND → HELM EXECUTION → RESULT

The actual routing may be dynamic. Not every event requires every Department. The AI Dispatcher determines which Departments are relevant to the incoming information.

---

## 14. Conflict Handling

A Department conflict is an operational state, not an error to be hidden.

Example:
NAVIGATOR Dpt.: "Intervention Required"
VS.
HELM Dpt.: "Action Cannot Be Executed"

Result:
CONFLICT DETECTED → DECISION BLOCKED / ESCALATION → CAPTAIN Dpt. → HUMAN AUTHORITY

The system shall preserve:
- conflicting assessments
- Department identities
- timestamps
- evidence
- reason for conflict
- resolution
- authority state

---

## 15. Authority Boundary

The architecture shall maintain an explicit boundary:

AI ANALYSIS → AI RECOMMENDATION → (AUTHORITY BOUNDARY) → HUMAN AUTHORITY → AUTHORIZED COMMAND → EXECUTION

Crossing the authority boundary without an explicit authority state is a structural violation.

---

## 16. Future Extension — Non-Intervention

The current contracts are primarily designed around positive operational control.

A future research extension shall address:

CONDITION DETECTED → INTERVENTION POSSIBLE → NO INTERVENTION → OPERATION CONTINUES → LATER AUDIT

The architecture must eventually determine how a legitimate non-intervention can become a verifiable operational state transition.

This problem is intentionally not solved by this document. The research question remains:

How can an operational system authenticate a legitimate non-intervention as an operational state transition when no physical intervention occurred?

---

## 17. Contract Integrity Principle

The purpose of these contracts is not to make the AI system more autonomous. The purpose is to make its operational boundaries more explicit.

The architecture shall therefore prefer:

DEFINED FUNCTION + DEFINED RESPONSIBILITY + DEFINED AUTHORITY + DEFINED RECORD

over:

GENERAL AI CAPABILITY

---

## 18. Version Control

Changes to Department contracts shall be version controlled.

Any change affecting:
- authority
- permitted recommendations
- prohibited decisions
- mandatory actions
- output schema
- decision dependencies

shall constitute a contract revision.

---

## 19. Final Architectural Rule

The INS Virtual Company shall operate according to the following principle:

AI may analyze.
AI may recommend.
Authority must remain explicit.
Execution must be controlled.
The decision pathway must remain visible.

The objective is:

FROM INFORMATION → TO DECISION → TO CONTROLLED ACTION → TO VERIFIABLE RECORD

---

**AVCS VIRTUAL COMPANY**
Adaptive Vector Control System
From information to decision.
From decision to controlled action.
From action to verifiable record.
