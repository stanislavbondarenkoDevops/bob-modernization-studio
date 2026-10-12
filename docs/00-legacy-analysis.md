# 00 — Legacy analysis: Hospital Management System (Flask, 2023)

Source: https://github.com/MAYANKpandey14/Hospital-Management-System — MIT, last commit 2023-03-19, single-file Flask app (`PROJECT/main.py`, 274 lines, 12 routes, 9 Jinja templates), MySQL dump `hmdbms.sql` (phpMyAdmin), no tests, no Dockerfile, no requirements.txt.

## Findings (baseline, to be confirmed by Bob Ask mode)
| # | Finding | Evidence | Severity |
|---|---------|----------|----------|
| 1 | SQL injection via f-string SQL in 8 statements | `db.engine.execute(f"... '{email}' ...")` lines 103–249 | Critical |
| 2 | Hardcoded secrets | `app.secret_key='mayank'`, Gmail creds in `MAIL_PASSWORD`, `mysql://root:@localhost` | Critical |
| 3 | Dead API: `db.engine.execute()` removed in SQLAlchemy 2.0; `User.query.get()` deprecated | imports + usage | Blocks upgrade |
| 4 | No dependency manifest — unreproducible build | repo root | High |
| 5 | Mixed ORM + raw SQL; models defined but bypassed | `class Patients(db.Model)` vs raw INSERT | High |
| 6 | No tests, no CI, no container | repo root | High |
| 7 | Unused import `from ast import Param`; `local_server` global | line 1 | Low |
| 8 | Passwords: werkzeug hash present (good), but user type from form input unchecked | `/signup` | Medium |

## Core functionality to preserve (regression contract)
Patient registration + edit + delete, doctor registration, appointment booking (slot/date/dept), login/signup with roles, trigger-log listing (`/details`). All 9 templates must render unchanged.
