from fastapi import FastAPI

from app.api.v1.api import api_router

app = FastAPI(title="LogiFlow")
app.include_router(api_router, prefix="/api/v1")
