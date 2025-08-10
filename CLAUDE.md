# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Bazi Energy MVP - a FastAPI-based web service that provides Chinese metaphysics Bazi (八字) interpretations. The system uses a rule-based engine to analyze Four Pillars of Destiny charts and provide energy-based interpretations.

## Development Commands

### Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Service
```bash
uvicorn app:app --reload
```
Service runs on http://127.0.0.1:8000 with auto-reload for development.

### Testing
```bash
pytest -q                    # Run all tests quietly
pytest -v                    # Run tests with verbose output
pytest test_ten_gods.py     # Run specific test file
```

### API Testing
```bash
curl -X POST "http://127.0.0.1:8000/interpret" \
  -H "Content-Type: application/json" \
  -d '{"bazi":"甲子 乙丑 丙寅 丁巳", "question":"我适合创业吗？"}'
```

### Docker
```bash
docker build -t bazi-energy-mvp .
docker run -p 8000:8000 bazi-energy-mvp
```

## Architecture

### Core Components
- `app.py`: FastAPI application with single `/interpret` endpoint
- `bazi_engine_d1d2.py`: Core rule engine containing Bazi interpretation logic
- `test_ten_gods.py`: Unit tests for ten-god relationship calculations

### Data Flow
1. FastAPI receives POST request to `/interpret` with bazi chart and optional question
2. Request validated via Pydantic model (`InterpretRequest`)
3. `interpret_bazi()` function from engine processes the bazi string
4. Response returns interpretation results or error details

### Key Functions
- `interpret_bazi(bazi: str, question: str)`: Main interpretation engine (currently incomplete - returns TODO)
- `determine_ten_god(day_gan: str, other_gan: str)`: Calculates ten-god relationships between heavenly stems

## Important Notes

- The engine currently contains only basic heavenly stem properties (`tian_gan_props`)
- Missing implementations noted in TODO comments: 地支藏干 (earthly branch hidden stems) and D1/D2 rule tables
- Rule engine is designed to encode PDF tables from "能量易学 第一级.pdf" as machine-readable dictionaries
- Production deployment would require integration with `sxtwl` or equivalent library for Gregorian-to-Ganzhi datetime conversion
- Domain experts should review `bazi_engine_d1d2.py` for final rule tuning

## Dependencies
- FastAPI: Web framework and API development
- Uvicorn: ASGI server with production-ready features
- Pydantic: Data validation and settings management
- Pytest: Testing framework
- Python-multipart: Form data handling
- Requests: HTTP client for health checks

## Production Configuration

### Environment Variables
Copy `.env.example` to `.env` and customize:
- `DEBUG`: Enable/disable debug mode
- `SECRET_KEY`: Security key for production
- `RATE_LIMIT_REQUESTS`: Requests per minute limit
- `LOG_LEVEL`: Logging verbosity

### Security Features
- CORS middleware with configurable origins
- Rate limiting (60 requests/minute by default)
- Input validation and sanitization
- Security headers (XSS protection, CSRF, etc.)
- Request logging and monitoring

### Deployment Options

#### Docker (Recommended)
```bash
# Build and run locally
docker-compose up --build

# Production build
docker build -t bazi-energy-mvp .
docker run -p 8000:8000 -e DEBUG=false bazi-energy-mvp
```

#### Railway
```bash
# Deploy with Railway CLI
railway up
```

#### Vercel
```bash
# Deploy with Vercel CLI
vercel --prod
```

#### Manual Deployment
```bash
pip install -r requirements.txt
python app.py
```

### Health Monitoring
- Health check endpoint: `/api/health`
- Application info: `/api/info`
- Built-in request logging and error tracking
- Docker health checks configured