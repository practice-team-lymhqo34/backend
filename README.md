# LogiFlow — Backend

> LogiFlow is a logistics management platform that helps teams track shipments,
> manage warehouses, and automate delivery workflows.

## Features

- User authentication (JWT)
- Shipment management
- Warehouse management
- REST API endpoints
- Database integration (PostgreSQL)

## Tech Stack

- Python 3.13
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Ruff + Black
- Pytest

## Getting Started

### Prerequisites

- Python >= 3.13
- PostgreSQL

### Installation

```bash
git clone https://github.com/practice-team-lymhqo34/backend.git
cd backend
python -m venv .venv
```

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / Mac

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
uv sync
```

### Running

```bash
uvicorn app.main:app --reload
Application will be available at:
http://127.0.0.1:8000
API docs:
http://127.0.0.1:8000/docs
```
