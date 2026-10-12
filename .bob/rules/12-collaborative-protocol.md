# Collaborative Protocol -- DevOps Studio

All director agents follow this mandatory workflow for every significant decision.

---

## Decision Cycle

Every significant decision follows this sequence:

```
Understand -> Analyze -> Options -> Approval -> Execute
```

Never skip a step. Never merge steps to save time. The sequence enforces that:
- The user is informed before anything is executed
- Options are real alternatives, not a single choice dressed as three
- Approval is explicit and selectable, not implied by silence

---

## Explain -> Capture Pattern

After producing an analysis, recommendation, or verdict:

1. **Explain** -- write the full analysis in plain text (what was found, what it means, what is recommended)
2. **Capture** -- call AskUserQuestion to present the decision as a selectable UI

Do NOT embed the decision question in the explanation text. Always make it a separate AskUserQuestion call.

### Standard sign-off options (use for all gates and approvals)

```
Use AskUserQuestion:
  question: "<summary of decision or finding>"
  tabs:
    - zatverdzhuyu (proceed with recommendation)
    - vidkhylyayu (reject, needs revision)
    - zapytannya (I have a question before deciding)
```

---

## Gate Verdict Format

The first line of every gate verdict must be a machine-parseable token:

```
[GATE-ID]: APPROVE
[GATE-ID]: CONCERNS -- <one-line summary>
[GATE-ID]: REJECT -- <one-line summary>
```

Do NOT write prose before the token. The token must be line 1.

After the token, provide:
- Checklist results (per gate-definitions.md)
- Explanation of CONCERNS or REJECT items
- Recommended remediation if not APPROVE

---

## Parallel Gate Execution (full mode)

At ARCH-DECISION and SEC-BASELINE gates, spawn all three directors simultaneously:

```
architect         -> ARCH-DECISION verdict
security-director -> SEC-BASELINE verdict
sre-director      -> SRE-READY pre-check
```

Verdict aggregation rule: **strictest verdict wins**.
- One REJECT overrides all APPROVEs -- combined result is REJECT
- One CONCERNS with all others APPROVE -- combined result is CONCERNS
- All APPROVE -- combined result is APPROVE

Present aggregated result to user with AskUserQuestion (standard zatverdzhuyu / vidkhylyayu / zapytannya tabs).

---

## Chain-of-Verification

Before finalizing any APPROVE verdict at a critical gate, generate 3 challenge questions
designed to disprove the verdict:

```
Challenge 1: What would make this APPROVE incorrect?
Challenge 2: What did I not check that could change this verdict?
Challenge 3: What is the worst-case scenario if this verdict is wrong?
```

Answer each question independently. If any answer reveals a gap, revise the verdict to
CONCERNS and document the gap. Only proceed with APPROVE if all 3 challenges are answered
without revealing unexamined risks.

---

## When to Apply This Protocol

- Every gate check (ARCH-DECISION, SEC-BASELINE, COST-ESTIMATE, ARCH-REVIEW, SRE-READY, SEC-SCAN, INCIDENT-RESOLVED)
- Every architecture decision that creates an ADR
- Every phase transition in a team skill that produces a plan or report
- Every recommendation that will result in infrastructure changes

---

## Reference

Gate definitions:  `.bob/gates/gate-definitions.md`
Verdict format:    `.bob/gates/verdict-format.md`
Delegation rules:  `docs/delegation-map.md`
