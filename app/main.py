from fastapi import FastAPI
from .database import engine, Base
from .routers import projects, places

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Travel Planner API")

app.include_router(projects.router)
app.include_router(places.router)