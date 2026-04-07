# LogiFlow — Backend

> LogiFlow backend is a REST API service that handles authentication, shipment management, warehouse operations, and
> core business logic for the logistics platform.

## Features

- User authentication (JWT)
- Shipment management
- Warehouse management
- REST API endpoints
- Database integration (PostgreSQL)

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Ruff + Black
- Pytest

## Getting Started

### Prerequisites

- Python >= 3.11
- PostgreSQL

### Installation

```bash
git clone <your-backend-repo-url>
cd backend

python -m venv .venv

### Windows
.venv\Scripts\activate

### Linux / Mac
source .venv/bin/activate

pip install -r requirements.txt
