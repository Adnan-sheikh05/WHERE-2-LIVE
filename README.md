# WhereToLive

A FastAPI + PostgreSQL backend that helps users compare Indian cities on
livability — cost of living, air quality, safety, and healthcare — with
AI-generated summaries and recommendations powered by Gemini.

## Features

- **City Data** — browse cities with year-wise livability metrics
- **Auth** — JWT-based signup/login, protected routes
- **Rankings** — overall and state-wise livability rankings (weighted scoring)
- **Compare** — side-by-side comparison of any two cities
- **AI Summary** — Gemini-generated natural-language comparison between two cities
- **AI Recommend** — describe your priorities, get a personalized city suggestion
- **Saved Comparisons** — logged-in users can save comparisons for later

## Tech Stack

| Layer          | Tool                                     |
| -------------- | ---------------------------------------- |
| Framework      | FastAPI                                  |
| Database       | PostgreSQL + SQLModel                    |
| Auth           | JWT (`python-jose`) + `passlib` (bcrypt) |
| External calls | `httpx` (async)                          |
| LLM            | Gemini API (`gemini-3.5-flash`)          |
| Deployment     | Render                                   |

## Project Structure

```
wheretolive/
├── app/
│   ├── main.py              # app entry point, router registration
│   ├── database.py          # engine + session setup
│   │
│   ├── models/               # SQLModel database tables
│   ├── schemas/               # request/response validation models
│   ├── routers/               # API route definitions
│   ├── services/               # business logic (auth, rankings, LLM)
│   ├── middlewares/            # request logging, etc.
│   │
│   └── seed/
│       ├── cities_seed.csv
│       └── seed_runner.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone and install

```bash
git clone https://github.com/<your-username>/wheretolive.git
cd wheretolive
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:

```
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
DB_NAME=wheretolive_db

JWT_SECRET=your-secret-key
GEMINI_API_KEY=your-gemini-key
```

### 3. Create the database

```sql
CREATE DATABASE wheretolive_db;
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

Tables are created automatically on startup. Visit `http://127.0.0.1:8000/docs`
for interactive API docs.

### 5. Seed sample city data

```bash
python -m app.seed.seed_runner
```

## API Overview

| Method | Endpoint                  | Description                              |
| ------ | ------------------------- | ---------------------------------------- |
| POST   | `/auth/signup`            | Create an account                        |
| POST   | `/auth/login`             | Get a JWT access token                   |
| GET    | `/auth/profile`           | Get current user (protected)             |
| GET    | `/cities`                 | List all cities                          |
| GET    | `/cities/{id}`            | Get a single city                        |
| GET    | `/cities/{id}/history`    | Year-wise metrics for a city             |
| GET    | `/rankings`               | Overall livability rankings              |
| GET    | `/rankings/state/{state}` | State-wise rankings                      |
| GET    | `/rankings/compare`       | Compare two cities                       |
| POST   | `/ai/summary`             | AI-generated comparison summary          |
| POST   | `/ai/recommend`           | AI-generated personalized recommendation |
| POST   | `/comparisons`            | Save a comparison (protected)            |
| GET    | `/comparisons/mine`       | View saved comparisons (protected)       |

Full interactive documentation is available at `/docs` once the server is running.

## Deployment

Deployed on [Render](https://render.com) — see `DEPLOYMENT.md` for step-by-step
instructions covering PostgreSQL setup, environment variables, and the web
service configuration.

## License

MIT
