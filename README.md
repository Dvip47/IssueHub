IssueHub – Lightweight Bug Tracker

IssueHub is a clean, minimal, and approachable bug-tracking system designed for small teams who want clarity without complexity. It pairs a FastAPI backend with a responsive React frontend, bundled neatly with Docker for an easy start.

Tech Stack

Backend: FastAPI, SQLAlchemy, Alembic, Pydantic, PostgreSQL

Frontend: React (Vite), Vanilla CSS, Axios, React Context

Database: PostgreSQL

Containerization: Docker Compose

Prerequisites

To run IssueHub, you’ll need either of the following:

Docker and Docker Compose

OR a local setup with Python 3.9+ and Node.js 18+

Quick Start with Docker

Spin it up

docker-compose up --build


Open the app

Frontend: http://localhost:5173

API Docs (Swagger): http://localhost:8000/docs

Run migrations
Migrations aren’t automated in this setup to keep things transparent and interview-friendly. Apply them manually:

docker-compose exec backend alembic upgrade head


Tip: Give the database a moment to finish initializing on the first run.

Load sample data

docker-compose exec backend python app/seed.py

Manual Setup
Backend

cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

Update .env or app/core/config.py with your PostgreSQL details

alembic upgrade head

Run the server:

uvicorn app.main:app --reload

Frontend

cd frontend

npm install

npm run dev

### Local Setup (SQLite / No Docker)

If you cannot use Docker or a local PostgreSQL instance, you can run the project with SQLite:

#### Backend

1. Navigate to backend:
   ```bash
   cd backend
   ```
2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment to use SQLite:
   ```
   DATABASE_URL=sqlite:///./issuehub.db
   ```
   (A sample `.env` with this value is provided).

5. Run migrations:
   ```bash
   alembic upgrade head
   ```
6. Seed data:
   ```bash
   PYTHONPATH=. python app/seed.py
   ```
7. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend

1. Navigate to frontend:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start development server:
   ```bash
   npm run dev
   ```

Known Limitations

Auth storage: JWT is stored in localStorage. Session persists on refresh.

Validation: Input rules are basic and intentionally lightweight.

Permissions: Only minimal role-based checks (Maintainer / Member).

Future Improvements

Persistent auth (cookies or localStorage)

Real-time updates via WebSockets

Email notifications for issue events

Rich-text editor for issue descriptions