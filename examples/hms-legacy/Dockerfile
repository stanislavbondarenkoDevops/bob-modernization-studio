# S0 baseline image — intentionally mirrors how the legacy app was run (no hardening yet; see ADR-001 S2)
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY PROJECT/ PROJECT/
ENV DATABASE_URL=sqlite:////data/hms.db
RUN mkdir -p /data
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--chdir", "PROJECT", "main:app"]
