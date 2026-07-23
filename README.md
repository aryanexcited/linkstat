# LinkStat

<p align="center">

# 🔗 LinkStat

A production-ready URL shortening service built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.  
LinkStat supports custom slugs, click analytics with a 7-day historical breakdown, Docker-based deployment, automated testing with Pytest, and Continuous Integration using GitHub Actions.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![Pytest](https://img.shields.io/badge/Tests-10%20Passing-brightgreen)
![CI](https://github.com/aryanexcited/linkstat/actions/workflows/ci.yml/badge.svg)

</p>

---

## Live Demo

**API**

https://linkstat-api.onrender.com

**Interactive Docs**

https://linkstat-api.onrender.com/docs

---

# Preview

<p align="center">
<img src="assets/hero.png" width="900">
</p>

---

# Features

- Collision-free Base62 short URLs
- Custom slugs
- Click analytics
- Seven-day traffic history
- Redirect tracking
- Dockerized deployment
- PostgreSQL persistence
- Alembic migrations
- Automated testing
- Continuous Integration

---

# Tech Stack

| Category | Technology |
|-----------|------------|
| Backend | FastAPI |
| Database | PostgreSQL (Neon) |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Validation | Pydantic |
| Testing | Pytest |
| CI/CD | GitHub Actions |
| Containerization | Docker |
| Deployment | Render |

---

# Architecture

```
                Client
                   │
                   ▼
             FastAPI Server
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
   URL Shortener      Analytics
          │                 │
          └────────┬────────┘
                   ▼
             PostgreSQL
         ┌─────────┴─────────┐
         │                   │
        urls              clicks
```

---

# Database Design

### urls

| Column | Description |
|---------|-------------|
| id | Primary Key |
| short_code | Unique Base62 Code |
| original_url | Original URL |
| created_at | Timestamp |
| user_id | Reserved for authentication |

### clicks

| Column | Description |
|---------|-------------|
| id | Primary Key |
| url_id | Foreign Key |
| clicked_at | Timestamp |
| referrer | Optional HTTP Referer |

The analytics system stores every click separately instead of maintaining a single counter, allowing historical traffic analysis and future reporting features.

---

# API Preview

## Swagger UI

<p align="center">
<img src="assets/swagger.png" width="900">
</p>

---

## Analytics

<p align="center">
<img src="assets/analytics.png" width="900">
</p>

---

# Local Setup

## Clone

```bash
git clone https://github.com/aryanexcited/linkstat.git
cd linkstat
```

## Configure

Create a `.env` file.

```env
DATABASE_URL=postgresql://postgres:password@localhost:5433/postgres
```

## Build

```bash
docker compose up --build
```

## Run migrations

```bash
alembic upgrade head
```

Open

```
http://localhost:8000/docs
```

---

# Running Tests

Run all automated tests

```bash
pytest -v
```

Current coverage includes:

- Health endpoint
- URL shortening
- Redirects
- Validation
- Error handling
- Analytics

---

# Continuous Integration

Every push automatically:

- Installs dependencies
- Runs all Pytest tests
- Reports build status

<p align="center">
<img src="assets/ci.png" width="900">
</p>

---

# Project Structure

```
linkstat/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── config.py
│   └── utils.py
│
├── tests/
│
├── alembic/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── keep-alive.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Future Improvements

- User authentication
- QR code generation
- Link expiration
- Rate limiting
- Redis caching
- Custom domains

---

# License

MIT License