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
- PostgreSQL 17
- SQLAlchemy
- Ruff + Black
- Pytest

## Getting Started

### Prerequisites

- Python >= 3.13
- PostgreSQL 17

### Installation

```bash
git clone https://github.com/practice-team-lymhqo34/backend.git
cd backend
uv venv
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
uvicorn src.server.main:app --host 0.0.0.0 --port 8000 --workers 4
API URL: http://127.0.0.1:8000
Swagger Docs: http://127.0.0.1:8000/docs
```
