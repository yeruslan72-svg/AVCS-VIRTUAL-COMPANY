# AVCS CODE OF PRACTICE

## Technical Standard for SIM Audits

**Version:** 1.1
**Status:** Binding Technical Standard — Frozen
**Effective Date:** September 2026
**Supersedes:** Code of Practice v1.0 (February 2026)
**Companion Documents:** AVCS Charter v1.1, CORE v2.1, Code of Ethics v1.1

---

## PREAMBLE

This Code of Practice is the technical standard for AVCS audits. It defines how SIM audits are planned, conducted, scored, and reported.

It is subordinate to the **AVCS Charter v1.1** and **CORE v2.1**, and operates under the **Code of Ethics v1.1**.

Where this Code and the Charter appear to conflict, the **Charter prevails in constitutional matters**.

Where this Code and the Code of Ethics appear to conflict, the **Code of Ethics prevails in ethical matters**.

Compliance with this standard is mandatory for all certified AVCS Practitioners.

---

## 1. SCOPE

This standard establishes requirements for:

- planning and conducting SIM audits,
- documenting evidence and observations,
- scoring structural integrity,
- delivering audit reports,
- maintaining professional conduct.

SIM audits assess the **structural integrity of decision architecture** in high-risk operations.

They do not replace technical standards, HSE systems, or operational procedures.

They evaluate the decision integrity of the system that operates those procedures.

---

## 2. DEFINITIONS

| Term | Definition |
|---|---|
| **SIM** | Structural Integrity Module — the diagnostic instrument for evaluating decision architecture. |
| **Practitioner** | An individual certified to conduct SIM audits. |
| **Pillar** | One of five structural dimensions assessed in a SIM audit. |
| **Audit** | A structured evaluation of an operational unit using the SIM framework. |
| **Observation** | A documented fact or pattern identified during the audit. |
| **Finding** | A conclusion drawn from one or more observations, linked to a specific pillar. |
| **Evidence** | Verifiable artifact that establishes a structural condition at or before the moment of the assessed act. |
| **Status** | A claimed state (Protected, Authorized, Controlled, Within North, Closed) — not a structural condition. |

---

## 3. EVIDENCE BEFORE STATUS

Practitioners must not accept a claimed status — **Protected, Authorized, Controlled, Within North, Closed** — as evidence of a structural condition.

For every pillar, the Practitioner must require evidence that existed **at or before the moment** of the assessed act.

For every critical state, three things must be independently establishable:

1. The **claimed status** — what the record says.
2. The **required structural condition** — what must actually be true.
3. The **evidence** — what can be independently verified.

If the condition behind the status cannot be shown, the pillar is scored as **structurally absent**.

**The diagnostic question is:**

> **Show me the condition behind the status.**

This principle is encoded in:

- Charter v1.1, Section 4.3
- CORE v2.1, Law 21
- Code of Ethics v1.1, Section 11

---

## 4. CONTROLLED DEGRADATION VS DRIFT

Not every reduction of margin requires an immediate stop. High-reliability operations often function within controlled degradation.

The structural difference:

- **Controlled degradation** — reduction of margin with explicit ownership, declared, reviewable.
- **Drift** — silent normalization without structural visibility.

The Practitioner must distinguish between the two.

The diagnostic questions are:

1. Is the reduction explicitly declared?
2. Is the residual risk assigned to a named decision owner?
3. Is the limitation documented and reviewable?
4. Is there a defined boundary for when continuation becomes non-permissible?

**Controlled limitation is governance.**
**An undeclared limitation is drift.**

The line between the two is rarely technical.

**It is architectural.**

---

## 5. PRACTITIONER REQUIREMENTS

### 5.1 Eligibility

To be eligible for certification, a candidate must:

- have a minimum of 5 years of operational experience in high-risk environments (offshore, maritime, aviation, energy, or equivalent),
- demonstrate understanding of decision-making under pressure,
- have no conflicts of interest that would impair objectivity.

### 5.2 Certification Process

Certification requires:

1. Completion of AVCS methodology training (approved curriculum).
2. Passing a written examination covering theory and application.
3. Successful completion of two supervised audits under an existing Practitioner.
4. Formal acceptance by the AVCS Practitioner Council (once established) or the Founder.

### 5.3 Recertification

Certification is valid for three years.

Recertification requires:

- Evidence of at least three completed SIM audits during the period.
- No substantiated violations of the AVCS Code of Ethics.
- Participation in Practitioner community activities.

---

## 6. AUDIT PREPARATION

### 6.1 Scope Definition

Prior to the audit, the Practitioner must:

- agree with the client on the operational unit or process to be assessed,
- define the boundaries of the audit (e.g., one asset, one shift, one function),
- document the scope in writing.

### 6.2 Document Review

The Practitioner must obtain and review, where available:

- relevant operating procedures,
- deviation logs (minimum 6 months),
- incident and near-miss reports,
- escalation records,
- previous audit findings (if any).

### 6.3 Scheduling

The audit must be scheduled to allow access to:

- operational personnel during or immediately after shifts,
- supervisors and managers with decision-making authority,
- key documentation and systems.

---

## 7. FIELDWORK REQUIREMENTS

### 7.1 Interviews

The Practitioner must conduct structured interviews with:

| Group | Minimum number |
|---|---|
| Operational personnel (operators, technicians) | 3 |
| Supervisors / shift leads | 2 |
| Management (HSE, Operations, Asset Integrity) | 1–2 |

Interviews must:

- follow the SIM Diagnostic Interview Guide,
- be documented anonymously,
- explore real scenarios, not hypotheticals,
- cross-check statements against documentation.

### 7.2 Documentation Review On Site

The Practitioner must verify:

- alignment between written procedures and actual practice,
- completeness of deviation logs,
- visibility of overrides,
- evidence of drift tracking (or absence thereof),
- **evidence behind claimed statuses**.

### 7.3 Observations

All observations must be:

- fact-based and specific,
- linked to one or more pillars,
- cross-validated where possible,
- documented in a format suitable for inclusion in the final report.

---

## 8. SCORING METHODOLOGY

### 8.1 Pillar Scores

Each of the five pillars is scored on a scale of 0 to 5:

| Score | Description |
|---|---|
| 0 | Structurally absent |
| 1 | Informal / inconsistent |
| 2 | Defined but discretionary |
| 3 | Defined and mostly applied |
| 4 | Mandatory and documented |
| 5 | Mandatory, enforced, and audited |

### 8.2 Scoring Basis

Each score must be justified by:

- specific observations,
- documented evidence,
- patterns identified across interviews.

Scores are not averages. They reflect the **dominant structural condition** of the system.

### 8.3 Total Structural Integrity Score

The total score is the sum of the five pillar scores (maximum 25).

### 8.4 Bands — Structural Conditions of Control

The bands correspond to the structural conditions of control defined in CORE v2.1, Law 10:

| Band | Classification | Structural Condition |
|---|---|---|
| 0–10 | High Structural Vulnerability | Multiple conditions of control fail. |
| 11–17 | Conditional Stability | Some conditions of control satisfied, others not. |
| 18–22 | Structurally Controlled | All conditions of control satisfied. |
| 23–25 | Architecturally Resilient | All conditions satisfied and structurally verified over time. |

---

## 9. REPORTING REQUIREMENTS

### 9.1 Mandatory Sections

Every SIM Audit Report must contain:

| Section | Content |
|---|---|
| **Executive Summary** | 1–2 pages summarizing key findings, total score, and primary vulnerabilities. |
| **Audit Scope and Methodology** | Description of the unit assessed, dates, and methods used. |
| **Pillar-by-Pillar Assessment** | Score, observations, evidence summary, and vulnerability for each pillar. |
| **Structural Vulnerability Map** | Narrative interpretation of risk concentration. |
| **Priority Reinforcement Plan** | Recommended actions with estimated complexity and timeline. |
| **Structural Risk Forecast** | Most likely failure scenario if no action is taken. |
| **Evidence Appendix** | Summary of evidence supporting each scored condition. |

### 9.2 Prohibited Content

The report must not contain:

- Individual blame or attribution of error to specific persons.
- Cultural generalizations unsupported by evidence.
- Technical recommendations outside the Practitioner's competence.
- **Acceptance of a claimed status without condition.**
- **Retroactive reconstruction of decision legitimacy.**
- **Presentation of assumption as evidence.**

### 9.3 Confidentiality

The report is the property of the client.

The Practitioner may not share it with third parties without written consent, except:

- anonymized for case study development (with client permission),
- for quality review by the AVCS Practitioner Council.

---

## 10. ETHICAL BOUNDARIES

### 10.1 Prohibited Conduct

A Practitioner must not:

- use audit data to evaluate or recommend action against individuals,
- accept compensation tied to audit outcomes,
- conduct audits where they have a conflict of interest (e.g., recent employment),
- misrepresent scores or findings,
- claim AVCS certification if lapsed or revoked,
- **accept a claimed status without condition**.

### 10.2 Independence

Practitioners must maintain independence from:

- operational pressure to alter findings,
- commercial incentives to soften conclusions,
- **organizational pressure to accept status as evidence of condition**.

---

## 11. AI IN AUDITS

Practitioners may use AI as an analytical instrument. AI may assist with data analysis, pattern detection, and structural assessment.

**AI does not score.**
**AI does not authorize.**
**AI does not replace human judgment.**

The Practitioner remains fully responsible for scoring, findings, and recommendations.

Recommendation is not authority. Analysis is not authorization. Capability is not permission.

---

## 12. SELF-APPLICATION

The Code of Practice is subject to the same structural integrity principles it imposes on audited systems.

Where the Practice diverges from the Charter, CORE, or Code of Ethics, the divergence is recorded as a **test result** — not as an automatic change to the governing documents.

AVCS has applied this principle to itself.

The **Architecture Reconciliation** (September 2026) tested the AVCS Virtual Company against Charter v1.1 and CORE v2.1, and detected **four recorded areas of structural divergence**. The Constitution remained unchanged. The implementation was reconciled.

This is not a claim. It is a **structural property** of the discipline.

---

## 13. QUALITY ASSURANCE

### 13.1 Practitioner Council

The AVCS Practitioner Council (once established) is responsible for:

- reviewing complaints and alleged violations,
- conducting random quality reviews,
- making recommendations on certification and revocation.

Until the Council is formally established, its functions are carried out by the Founder — except in matters concerning the Founder, which are adjudicated by a panel of three senior Practitioners.

The composition, procedures, and mandate of the Council are defined in a separate document: **AVCS Practitioner Council Charter**.

### 13.2 Complaints

Any client or Practitioner may file a complaint regarding:

- suspected violation of this Code of Practice,
- breach of the AVCS Code of Ethics,
- professional misconduct.

Complaints are reviewed by the Council. The accused Practitioner has the right to respond.

### 13.3 Sanctions

Sanctions may include:

- written warning,
- requirement to undergo additional training,
- suspension of certification (temporary),
- revocation of certification (permanent).

Revocation requires a two-thirds majority of the Council (excluding the accused) and may be appealed to the Founder.

---

## 14. RESEARCH PARTICIPATION

Where Practitioners participate in AVCS research — including joint boundary tests, drift detection, and convergence studies — the following principles apply:

- Findings must be provisional until tested.
- Convergence must be recorded, not absorbed.
- Provenance must be preserved.
- External contributions must be attributed.
- Frameworks must not be silently collapsed into one another.

Research findings do not automatically become AVCS doctrine. They become **test results**. Doctrine is amended only through the process defined in the Charter and CORE.

---

## 15. VERSION AND EVOLUTION

This is **Version 1.1** of the AVCS Code of Practice.

It may be amended by:

- the Founder, during the initial phase (first 10 Practitioners),
- the Practitioner Council, by two-thirds majority, thereafter.

Substantive changes require:

- documentation of the reason for change,
- identification of the source architecture (if from joint work or external convergence),
- preservation of provenance,
- review by the Practitioner Council (once established),
- two-thirds majority approval.

Substantive changes are communicated to all active Practitioners.

---

## STATUS OF THIS DOCUMENT

This Code of Practice is the technical standard for AVCS audits.

It is subordinate to the **AVCS Charter v1.1** and **CORE v2.1**, and operates under the **Code of Ethics v1.1**.

Where this Code and the Charter appear to conflict, the Charter prevails in constitutional matters.

Where this Code and the Code of Ethics appear to conflict, the Code of Ethics prevails in ethical matters.

**Version 1.1 — Frozen.**

---

**Issued by:**
Yeruslan Chihachyov
Founder — AVCS DNA MATRIX SPIRIT

**September 2026**
