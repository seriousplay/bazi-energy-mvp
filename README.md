# Bazi Energy MVP

This repository contains an MVP for a Bazi (八字) based energy interpretation service.

## What's inside
- `bazi_engine_d1d2.py`: Core rule engine (D1 + D2) with encoded tables and full ten-god logic.
- `app.py`: FastAPI service exposing `/interpret` endpoint.
- `test_ten_gods.py`: Pytest unit tests for ten-god logic.
- `Dockerfile`: Simple containerization.

## Quick start (local)

1. create a virtualenv and install:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. run service:

```bash
uvicorn app:app --reload
```

3. test api:

```bash
curl -X POST "http://127.0.0.1:8000/interpret" -H "Content-Type: application/json"   -d '{"bazi":"甲子 乙丑 丙寅 丁巳", "question":"我适合创业吗？"}'
```

4. run unit tests:

```bash
pytest -q
```

## Notes

- The engine encodes PDF/作业纸 tables as JSON-like literals in the code. Please have domain experts review `bazi_engine_d1d2.py` for final rule tuning.
- For production use, integrate `sxtwl` or an equivalent library to convert Gregorian datetime -> 干支 with correct 节气 and south-hemisphere handling.
