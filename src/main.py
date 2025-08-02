from fastapi import FastAPI
from src.api import endpoints
import os

app = FastAPI(
    title="Todo API",
    version="0.1.0",
)

app.include_router(endpoints.checklist.router, prefix="/api/v1")