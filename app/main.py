from fastapi import FastAPI
from app.api.routers import health, tasks

app = FastAPI(title="Tasky API")

app.include_router(health.router)
app.include_router(tasks.router)
