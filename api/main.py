from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from discord_oauth import flask_app
from fastapi.middleware.wsgi import WSGIMiddleware

from apis.base import api_router
from core.config import settings
from db.base_class import Base
from db.session import engine


def create_tables():
    Base.metadata.create_all(bind=engine)


def include_router(app):
    app.include_router(api_router)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    include_router(app)
    return app


app = start_application()

origins = [
    "http://localhost",
    "http://localhost:5000",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://swadebot.api:8000/api",
    "http://127.0.0.1",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
    "http://69.130.82.233",
    "http://69.130.82.233:5000",
    "http://69.130.82.233:5173",
    "http://69.130.82.233:8000",
    "http://69.130.82.233:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"msg": "Hello FastAPI🚀"}


app.mount("", WSGIMiddleware(flask_app))
