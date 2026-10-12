# Bob Modernization Studio

Governed multi-agent modernization workflow for IBM Bob, applied to a real legacy application.
Track: Modernize What Matters — IBM Bob Hackathon (AngelHack), Oct 2026.

## What it is
- `.bob/custom_modes.yaml` — 5 modes with tool-scoped permissions: session-director (orchestrator), architect, security-director, sre-director, modernizer.
- `.bob/rules/` — studio loop, gate definitions, verdict format, collaborative protocol.
- `.bob/rules-<mode>/` — per-mode role definitions (ported from a Claude Code multi-agent studio).
- `.bob/skills/` — gate-check, modernization-plan.
- `examples/<legacy-app>/` — the application modernized through the studio; git history is the evidence.
- `docs/adr/`, `docs/verdicts/`, `docs/bob-workflow/` — ADRs, gate verdicts, Bob transcripts and Bobalytics export.

## Workflow
1. Session Director (Plan) → decomposes task, dispatches Architect.
2. Architect → ADR + modernization plan → `[ARCH-DECISION]` verdict.
3. User: zatverdzhuyu.
4. Modernizer (Agent) → step-by-step upgrade, tests green after each step.
5. Security Director + SRE Director in parallel → `[SEC-BASELINE]`, `[SRE-READY]`.
6. Strictest verdict wins → deploy demo.

## Status
Legacy app: examples/hms-legacy — Flask Hospital Management System (MIT, 2023). See docs/00-legacy-analysis.md and docs/adr/ADR-001-modernization-path.md.
