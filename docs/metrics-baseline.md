# Metrics — baseline (v0-baseline, S0)

Measured 2026-10-13 on examples/hms-legacy with Python 3.10, bandit 1.8.0, pip-audit 2.7.3.

| Metric | Baseline | Target after S3 |
|---|---|---|
| Python | 3.11 (image) / 3.10 (local) | 3.13 |
| Flask / Werkzeug | 2.2.5 / 2.2.3 | 3.1.x / 3.1.x |
| SQLAlchemy / Flask-SQLAlchemy | 1.4.46 / 2.5.1 | 2.0.x / 3.1.x |
| Known CVEs in deps (pip-audit) | **11** (flask 1, werkzeug 8, gunicorn 2) | 0 |
| Bandit findings | 1 High (debug=True), 7 Medium (B608 SQLi), 2 Low (hardcoded creds) | 0 High/Medium |
| Raw f-string SQL statements | 8 | 0 |
| Hardcoded secrets | 3 (secret_key, gmail password, mysql root) | 0 |
| Tests | 17 passed, 3 xfail (characterization) | 17 + security + API contract |
| Known runtime bug | booking POST crashes (`ast.Param` misuse) | fixed |
| Container | root, python:3.11-slim, no healthcheck | non-root, healthcheck, pinned |
| JSON / FHIR API | none | /api/v1/patients, /fhir/Patient/{id} |
