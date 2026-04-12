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
  main.py                # FastAPI application and routes
  models.py              # API request models
  risk_logic.py          # Core risk scoring logic
  data_sources.py        # External/CSV data adapters
  tests/                 # Unit and API tests
```

## CI

GitHub Actions runs:

- Ruff
- Mypy
- Pytest with coverage enforcement

on both push and pull requests.

## Next Architecture Steps

- Introduce clean architecture layers (`api`, `application`, `domain`, `infrastructure`)
- Add dependency injection boundaries for external providers
- Expand model-serving and observability workflows