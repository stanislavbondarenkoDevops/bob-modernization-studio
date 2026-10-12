---
name: gate-check
description: "Manually run a specific quality gate check. Use to validate readiness before a critical operation or to check if a previous gate result is still valid."
argument-hint: "[GATE-ID: ARCH-DECISION|SEC-BASELINE|COST-ESTIMATE|ARCH-REVIEW|SRE-READY|SEC-SCAN|INCIDENT-RESOLVED]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Task, AskUserQuestion
context: |
  !cat production/review-mode.txt 2>/dev/null || echo "full"
  !cat .claude/gates/gate-definitions.md 2>/dev/null
---

## /gate-check [GATE-ID]

Manual gate validation. Use before critical operations or to verify readiness.

---

## Phase 1: Gate Selection

If GATE-ID provided, proceed to Phase 2.

Otherwise, use AskUserQuestion:
```
Which gate would you like to check?
```
options:
  - ARCH-DECISION — Architecture decision readiness
  - SEC-BASELINE — Security baseline readiness
  - COST-ESTIMATE — Cost estimation completeness
  - ARCH-REVIEW — Implementation review readiness
  - SRE-READY — SRE and monitoring readiness
  - SEC-SCAN — Security scan validation
  - INCIDENT-RESOLVED — Incident resolution verification

---

## Phase 2: Load Gate Definition

Read `.claude/gates/gate-definitions.md`.
Load the specific gate definition for the selected GATE-ID.
Read `production/review-mode.txt`.

---

## Phase 3: Pre-Check Context

Check for relevant artifacts:

**ARCH-DECISION:**
- Look for `docs/decisions/adr-*.md` (most recent)
- Check that alternatives section is populated
- Verify cost impact section exists

**SEC-BASELINE:**
- Look for `docs/decisions/security-baseline-*.md`
- Check IAM strategy section

**COST-ESTIMATE:**
- Look for `docs/decisions/cost-estimate-*.md`
- Check for monthly estimate figures

**ARCH-REVIEW:**
- Look for `terraform/` or `k8s/` directories
- Check for recent file modifications

**SRE-READY:**
- Look for `docs/decisions/slo-*.md`
- Check for `monitoring/prometheus/rules/`

**SEC-SCAN:**
- Look for recent scan reports in `production/session-logs/sec-scan-*.md`
- Check scan date (is it fresh enough?)

**INCIDENT-RESOLVED:**
- Look for `production/session-logs/incident-*.md`
- Check incident status field

---

## Phase 4: Gate Execution

Read review mode:

**solo mode:**
- Self-check all gate criteria
- Produce verdict without spawning agents

**lean mode:**
- For ARCH-DECISION, ARCH-REVIEW: spawn `architect`
- For SEC-BASELINE, SEC-SCAN: spawn `security-director`
- For SRE-READY: spawn `sre-director`
- For COST-ESTIMATE: self-check
- For INCIDENT-RESOLVED: self-check

**full mode — standard gates (COST-ESTIMATE, ARCH-REVIEW, SRE-READY, SEC-SCAN, INCIDENT-RESOLVED):**
- Spawn the gate owner agent (per gate definition)
- Gate owner runs through full checklist
- Produce formal verdict

**full mode — critical gates (ARCH-DECISION, SEC-BASELINE):**
Spawn all three directors simultaneously:

```
Spawn in parallel:
  - architect         via Task -> ARCH-DECISION verdict
  - security-director via Task -> SEC-BASELINE verdict
  - sre-director      via Task -> SRE-READY pre-check
```

Wait for all three verdicts. Apply strictest wins rule:
- Any REJECT -> aggregate is REJECT
- Any CONCERNS (no REJECT) -> aggregate is CONCERNS
- All APPROVE -> aggregate is APPROVE

---

## Phase 4b: Chain-of-Verification

After collecting verdict(s), before presenting to user:

Generate 3 challenge questions designed to disprove the aggregate verdict:
```
Challenge 1: What would make this verdict incorrect?
Challenge 2: What did the checklist not examine that could change this verdict?
Challenge 3: What is the worst-case scenario if this verdict is wrong?
```

Answer each independently. If any answer reveals an unexamined risk:
- Upgrade APPROVE -> CONCERNS and document the gap
- Upgrade CONCERNS -> REJECT if the gap is a blocking issue

---

## Phase 5: Verdict Presentation

Present gate result:

```
Gate: <GATE-ID>
Owner: <agent>
Date: YYYY-MM-DD HH:MM UTC

Checklist:
  [PASS] <criterion 1>
  [PASS] <criterion 2>
  [FAIL] <criterion 3> -- MISSING: <what's missing>
  [WARN] <criterion 4> -- CONCERN: <description>

Chain-of-Verification:
  Challenge 1: <question> -> <answer>
  Challenge 2: <question> -> <answer>
  Challenge 3: <question> -> <answer>

[GATE-ID]: APPROVE | CONCERNS -- <summary> | REJECT -- <summary>
```

"May I write the gate result to `production/session-logs/YYYY-MM-DD.md`?"

Log gate result to `production/session-logs/YYYY-MM-DD.md`.

Use AskUserQuestion:
```
question: "Gate <GATE-ID> check complete. Review verdict and confirm."
tabs:
  - zatverdzhuyu -- accept verdict, proceed
  - vidkhylyayu -- reject verdict, needs revision
  - zapytannya -- I have a question
```

---

## Phase 6: Resolution (if not APPROVE)

If CONCERNS or REJECT:

Use AskUserQuestion:
```
Gate <GATE-ID> is not APPROVE. How would you like to proceed?
```
options:
  - Address issues now (spawn relevant agent)
  - Override with justification (document reason)
  - Defer (log as known issue, continue at risk)

---

Verdict: **COMPLETE** — gate check complete.
Next Steps: Run `/terraform-apply` if ARCH-REVIEW APPROVE, `/team-new-env` if ARCH-DECISION APPROVE, `/team-incident` if INCIDENT-RESOLVED APPROVE.
