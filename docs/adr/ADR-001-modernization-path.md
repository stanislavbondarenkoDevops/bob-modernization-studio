# ADR-001 — Modernization path for Hospital Management System

Status: PROPOSED (awaiting [ARCH-DECISION] verdict) · Date: 2026-10-13 · Owner: architect

## Context
Legacy single-file Flask HMS (see docs/00-legacy-analysis.md). Hackathon track "Modernize What Matters" — transform without disrupting core functionality. 5 days, 1 engineer, IBM Bob as the workflow engine.

## Decision
Incremental strangler modernization in 4 steps, each gated, each leaving the app runnable:

| Step | Change | Proof it still works |
|------|--------|----------------------|
| S0 Baseline | Add `requirements.txt` (pinned as-found: Flask 2.x, Flask-SQLAlchemy 2.x, SQLAlchemy 1.4), Dockerfile, SQLite fallback, characterization tests via Flask test client for all 12 routes | tests green on legacy code |
| S1 Security | Replace 8 f-string SQL with ORM/parameterized queries; secrets → env vars; role whitelist on signup | SQLi tests (payloads from OWASP) return 0 rows; gitleaks clean |
| S2 Platform | Python 3.13, Flask 3.x, SQLAlchemy 2.x (`db.session.execute(select(...))`), app factory, blueprints (auth / patients / doctors / booking), Pydantic v2 settings | characterization tests green, pip-audit 0 CVE |
| S3 API enablement | `/api/v1/patients` JSON + **FHIR R4 Patient** read endpoint (`/fhir/Patient/{id}`), OpenAPI via flask-smorest | contract tests; FHIR resource validates against R4 schema |

Cut order if time runs out: S3 FHIR → S3 OpenAPI → S2 blueprints. S0–S1 are non-negotiable.

## Alternatives
1. Rewrite to FastAPI — rejected: breaks Jinja UI, violates "without disrupting core functionality", judges penalize rewrite-as-modernization.
2. Django migration — rejected: full rewrite, >5 days.
3. Keep Flask 2 / SQLAlchemy 1.4, security fixes only — rejected: no platform modernization story, weak on "framework upgrades".

## Consequences
- Cost: 0 infra beyond a Fly.io/EC2 demo container.
- Security: SEC-BASELINE gate after S1 and S3.
- Rollback: each step is a tagged commit (`v0-baseline`, `v1-secure`, `v2-platform`, `v3-api`); `git checkout` + `docker build`.
- SLO: /health endpoint added in S0; SRE-READY gate after S2.

## Bob usage per step (evidence for judges)
S0: Ask mode legacy explanation → this doc. S1–S3: session-director (Plan) → architect verdict → modernizer (Agent) with `fileRegex` limited to `examples/hms-legacy/`; security-director + sre-director as parallel subagents. Transcripts in docs/bob-workflow/, Bobalytics CSV export at the end.
