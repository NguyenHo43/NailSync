# NailSync

A nail salon management system built with FastAPI and PostgreSQL.

🚀 **Live Demo:** https://nailsync-production.up.railway.app/docs

## Features

- **Authentication** — JWT-based login with role-based access (Owner, Manager, Employee)
- **Employee Management** — CRUD, soft delete, salary calculation by month
- **Customer Management** — tracking with loyalty stamp system and birthday discount
- **Service Catalog** — categorized services (hand, foot, addon) with soft delete
- **Turn Management** — track services per turn, checkout with auto total calculation
- **Loyalty System** — stamp discount ($10 off every 10 visits) and birthday discount (10% off)
- **Automated Tests** — 15 pytest tests with isolated test database

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL + SQLAlchemy
- **Auth:** JWT (python-jose, bcrypt)
- **Testing:** pytest, httpx
- **Deployment:** Railway

## Setup

1. Clone repo
2. Create virtual environment: `python -m venv .venv`
3. Activate: `source .venv/bin/activate`
4. Install: `pip install -r requirements.txt`
5. Create: `.env`
6. Run server: `uvicorn app.main:app --reload`
7. Seed data: `python -m app.seed`
8. Run tests: `pytest tests/`
