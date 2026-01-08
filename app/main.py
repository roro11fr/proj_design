from fastapi import FastAPI
from app.api.routers import health, tasks

import logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Tasky API")

app.include_router(health.router)
app.include_router(tasks.router)
