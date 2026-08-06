# NailSync

A full-stack nail salon management system, built from firsthand experience working the front and back of a nail salon myself. NailSync handles staff scheduling, customer loyalty, service checkout, and the turn rotation queue salons use to assign the next available technician — problems I lived with before I ever wrote a line of code for them.

🚀 **Live demo:** [https://nailsync-1.onrender.com](https://nailsync-1.onrender.com)
📄 **API docs:** [https://nailsync.onrender.com/docs](https://nailsync.onrender.com/docs)

> ⚠️ Both are hosted on Render's free tier. The backend spins down after 15 minutes of inactivity — the first request may take 30–60 seconds to wake up. The database also resets every 30 days on the free tier; if login fails unexpectedly, it likely needs reseeding (`python3 -m app.seed`).

## Why this project

Before switching to Computer Science, I worked in nail salons. Turn order, loyalty tracking, and checkout math were all handled by memory or paper — and disputes over whose turn it was were common. NailSync is my attempt to solve problems I actually lived with, using what I am learning now.

## Features

- **Authentication** — JWT-based login with role-based access (Owner, Manager, Employee)
- **Employee management** — CRUD, soft delete, monthly salary calculation
- **Customer management** — loyalty stamp system and birthday discounts
- **Service catalog** — categorized services (hand, foot, addon) with soft delete
- **Turn management** — track services per turn, checkout with automatic total calculation
- **Loyalty system** — stamp discount ($10 off every 10 visits), birthday discount (10% off)
- **Auto queue management** — automatic employee assignment based on skill level, availability, and check-in order
- **Employee check-in/check-out** — daily queue management with automatic turn order assignment
- **Automated tests** — 16 pytest tests with an isolated test database
- **Frontend (in progress)** — React login flow and employee list, styled with Tailwind + shadcn/ui

## Tech stack

**Backend**
- FastAPI (Python)
- PostgreSQL + SQLAlchemy
- JWT auth (python-jose, bcrypt)
- pytest + httpx for testing

**Frontend**
- React + Vite
- Tailwind CSS
- shadcn/ui component library

**Deployment**
- Render (Web Service for backend, Static Site for frontend, managed PostgreSQL)

## Running locally

**Backend**
```bash
git clone https://github.com/NguyenHo43/NailSync.git
cd NailSync
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
DATABASE_URL=postgresql://username@localhost:5432/nailsync
SECRET_KEY=your-secret-key
```

```bash
uvicorn app.main:app --reload
python3 -m app.seed      # populate sample data
pytest tests/             # run the test suite
```

**Frontend**
```bash
cd frontend
npm install
```

Create a `.env` file in `frontend/`:
```
VITE_API_URL=http://localhost:8000
```

```bash
npm run dev
```

## Project structure

```
NailSync/
├── app/                # FastAPI backend
│   ├── models/           # SQLAlchemy models (employee, customer, service, turn...)
│   ├── routers/           # API routes
│   ├── schemas/           # Pydantic schemas
│   ├── auth.py            # Password hashing, JWT logic
│   ├── database.py         # DB connection/session setup
│   ├── main.py             # App entrypoint, CORS, routers
│   └── seed.py             # Sample data seeding
├── frontend/            # React + Vite frontend
│   └── src/
│       ├── components/      # LoginForm, EmployeeList, ui/ (shadcn)
│       └── App.jsx
└── tests/               # 16 pytest tests, isolated test database
```

## Roadmap

- [ ] Customer management UI
- [ ] Service and checkout UI
- [ ] Employee check-in/check-out UI
- [ ] Alembic migrations (currently relies on `Base.metadata.create_all`)

## Author

Rio (Nguyen Ho) — Computer Science student at the University of Oklahoma
[GitHub](https://github.com/NguyenHo43)
