# Session state
- 2026-10-13: scaffold created; modes + rules ported; legacy app not yet selected.
- 2026-10-13: legacy app selected (hms-legacy); ADR-001 proposed, awaiting ARCH-DECISION.
- 2026-10-13: S0 done — requirements (as-found pins), Dockerfile, env DATABASE_URL, __main__ guard, 20 characterization tests (17 pass / 3 strict xfail), baseline metrics in docs/metrics-baseline.md. Repo pushed to github.com/stanislavbondarenkoDevops/bob-modernization-studio, tag v0-raw.
- 2026-10-13: SEC-BASELINE CI pipeline adapted from devsecops-demo (.github/workflows/sec-baseline.yml), gates-ledger.md defines hard/soft per tag.
