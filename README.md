MarketBridge - Retail Supply Chain Optimizer

This is a minimal, runnable prototype of the MarketBridge platform. It includes a small FastAPI backend that serves a basic HTML dashboard and simple JSON APIs for inventory and predictions. The project uses SQLite for simplicity so you can run it locally without external services.

Quick start (PowerShell):

# create venv, install deps, run tests, start server
python -m venv .venv; .\.venv\Scripts\pip.exe install -r backend\requirements.txt; .\.venv\Scripts\pytest -q; .\.venv\Scripts\uvicorn.exe backend.app.main:app --reload --port 8000

Open http://127.0.0.1:8000 in your browser.

Notes & assumptions:
- For speed and portability this prototype uses SQLite instead of PostgreSQL.
- Authentication and production hardening are intentionally minimal.
- The predictive model is a simple moving-average heuristic as a placeholder.

Files of interest:
- backend/app/main.py: FastAPI application
- backend/app/models.py: SQLAlchemy models
- backend/app/schemas.py: Pydantic schemas
- backend/app/crud.py: DB helpers
- backend/app/predictor.py: simple predictor
- backend/templates/index.html: minimal UI
- backend/tests/test_api.py: basic tests

