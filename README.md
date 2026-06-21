# linkstat

A URL shortener with real click analytics — not just a counter, but a time-series breakdown of traffic per link, backed by a proper relational schema.

**Live demo:** https://linkstat-api.onrender.com/docs

## Features

- Shorten any URL via base62-encoded auto-increment IDs (collision-free by construction)
- Optional custom slugs (3–20 chars, alphanumeric + hyphen/underscore, with reserved-word protection)
- Every redirect logs a click event (timestamp + referrer) to a separate `clicks` table
- `/stats/{short_code}` aggregates total clicks and a zero-filled 7-day time series — built for charting, not just a raw count
- Fully containerized: API + PostgreSQL run together via Docker Compose
- Schema-versioned with Alembic migrations

## Tech Stack

FastAPI · PostgreSQL · SQLAlchemy · Alembic · Docker · Docker Compose · deployed on Render

## Architecture

**`urls`** — id, short_code (unique), original_url, created_at, user_id (nullable, for future auth)
**`clicks`** — id, url_id (FK → urls), clicked_at, referrer (nullable)

Click logging and stats aggregation are separated into their own table specifically so analytics can scale beyond a single counter column — `/stats` does a real `GROUP BY` query against `clicks`, not a cached number.

## Getting Started (local)

**Prerequisites:** Docker + Docker Compose

1. Clone the repo:
```bash
   git clone https://github.com/aryanexcited/linkstat.git
   cd linkstat
```

2. Create a `.env` file in the project root:
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5433/postgres

3. Update `docker-compose.yml`'s `POSTGRES_PASSWORD` to match, then start everything:
```bash
   docker compose up -d --build
```

4. Run database migrations:
```bash
   alembic upgrade head
```

5. The API is now running at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

## API Endpoints

### `POST /shorten`
Create a short URL, optionally with a custom slug.

**Request:**
```json
{
  "original_url": "https://www.anthropic.com",
  "custom_slug": "anthropic"
}
```
*(`custom_slug` is optional — omit it for an auto-generated base62 code)*

**Response (201):**
```json
{
  "short_code": "anthropic",
  "original_url": "https://www.anthropic.com/",
  "short_url": "https://linkstat-api.onrender.com/anthropic",
  "created_at": "2026-06-21T15:34:11.381745Z"
}
```

### `GET /{short_code}`
Redirects (302) to the original URL and logs a click event.

### `GET /stats/{short_code}`
Returns total clicks and a 7-day daily breakdown.

**Response:**
```json
{
  "short_code": "1",
  "original_url": "https://www.anthropic.com/",
  "total_clicks": 4,
  "clicks_last_7_days": [
    {"date": "2026-06-15", "clicks": 0},
    {"date": "2026-06-16", "clicks": 0},
    {"date": "2026-06-17", "clicks": 0},
    {"date": "2026-06-18", "clicks": 0},
    {"date": "2026-06-19", "clicks": 0},
    {"date": "2026-06-20", "clicks": 0},
    {"date": "2026-06-21", "clicks": 4}
  ]
}
```

### `GET /health`
Basic liveness + DB connectivity check.

## Stats Output

![stats screenshot](stats_screenshot.png)

## Project Structure
linkstat/

├── app/

│   ├── main.py        # routes

│   ├── models.py       # SQLAlchemy models

│   ├── schemas.py       # Pydantic request/response schemas

│   ├── database.py      # DB engine/session setup

│   ├── config.py        # env-based settings

│   └── utils.py         # base62 encoder

├── alembic/             # migration history

├── Dockerfile

├── docker-compose.yml

└── requirements.txt