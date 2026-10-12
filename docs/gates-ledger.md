# Gates ledger — which CI gates are hard, and from which tag

| Gate (job/step) | Tool | v0-baseline | v1-secure | v2-platform | v3-api |
|---|---|---|---|---|---|
| secrets | gitleaks (full history) | hard | hard | hard | hard |
| sast | bandit -ll, semgrep OWASP | soft | **hard** | hard | hard |
| sca | pip-audit --strict | soft | soft | **hard** | hard |
| test | pytest characterization | hard | hard | hard | hard |
| container/trivy | HIGH/CRITICAL fixable | soft | soft | **hard** | hard |
| container/dast | ZAP baseline (-I, informational) | info | info | info | **hard** |

Rule: a `continue-on-error: true` line may exist only with a `GATE-LEDGER:` comment naming the tag that removes it.
Removing the line is part of that step's Definition of Done and is checked by sre-director at SRE-READY.
