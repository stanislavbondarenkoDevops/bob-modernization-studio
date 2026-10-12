# Bob Modernization Studio — core rules

Loop for every task: READ → ANALYZE → PROPOSE → VALIDATE → EXECUTE → VERIFY → REPORT.
Two-phase confirmation: PHASE 1 analyze/propose → user says zatverdzhuyu / vidkhylyayu → PHASE 2 execute. No file changes without approval.
Gates: ARCH-DECISION (architect), SEC-BASELINE (security-director), SRE-READY (sre-director). Strictest verdict wins: REJECT > CONCERNS > APPROVE.
Max 2 revision cycles per gate, then escalate to the user.
Every verdict is written to docs/verdicts/<YYYY-MM-DD>-<GATE>.md in the format from 11-verdict-format.md.
Session state lives in docs/session-state.md — update it at the end of every session.
