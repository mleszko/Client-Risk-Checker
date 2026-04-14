# AI Risk Assessment Microservice

A Python microservice that evaluates client risk based on:

- business industry
- text risk signals in client descriptions
- optional enrichment from OpenCorporates company data

This repository is intentionally structured to evolve toward a portfolio-grade, production-oriented AI service.

## Tech Stack

- Python
- FastAPI
- Pydantic
- HTTPX
- Pandas / scikit-learn (for model-related workflows)
- Pytest + Coverage
- Ruff (linting/import formatting)
- Mypy (static type checks)

## Quick Start

1. Install dependencies:

   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run the API locally:

   ```bash
   python3 run.py
   ```

3. Call the endpoint:

   ```bash
   curl -X POST "http://127.0.0.1:8000/check_risk" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Acme Corp",
       "industry": "crypto",
       "description": "A startup under investigation for money laundering."
     }'
   ```

## Quality Gates

Run all local checks:

```bash
python3 -m ruff check .
python3 -m mypy
python3 -m pytest
```

The test suite enforces a minimum coverage threshold of **85%**.

## Project Structure

```text
app/
  main.py                         # FastAPI app bootstrap
  api/routes/risk.py              # HTTP route layer
  api/dependencies.py             # Dependency injection wiring
  application/services/           # Use-case orchestration
  domain/services/                # Pure domain rules/strategies
  infrastructure/company_data.py  # External data adapters
  models.py                       # Legacy API model (compat)
  risk_logic.py                   # Legacy compatibility wrapper
  data_sources.py                 # Legacy compatibility wrapper
  tests/                 # Unit and API tests
```

## CI

GitHub Actions runs:

- Ruff
- Mypy
- Pytest with coverage enforcement

on both push and pull requests.

## Architecture Notes

- This service now uses a clean layered architecture:
  - **API layer** (`app/api`): request/response boundary
  - **Application layer** (`app/application`): orchestration use-case
  - **Domain layer** (`app/domain`): pure risk rules + scoring strategy
  - **Infrastructure layer** (`app/infrastructure`): OpenCorporates adapter
- The `/check_risk` contract is preserved while internals are now DI-driven and
  easier to test, replace, and evolve.