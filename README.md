# NailSync

Nail salon management system built with FastAPI and PostgreSQL.

## Features
- Employee management
- Customer tracking
- Turn-based service tracking
- Automated salary and tip calculation

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Python 3.x

## Setup
1. Clone repo
2. Create virtual environment: `python -m venv .venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Create `.env` file with `DATABASE_URL`
5. Run: `uvicorn app.main:app --reload`
