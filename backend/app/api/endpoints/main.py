
from fastapi import FastAPI

from app.api.endpoints.hotels import router

from sqlalchemy.orm import Session
from app.database import models, database

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with PostgreSQL!"}
