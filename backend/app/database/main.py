from fastapi import FastAPI
from sqlalchemy.orm import Session
from . import models, database
import os

app = FastAPI()


@app.on_event("startup")
def startup():
    print("startup")
    models.Base.metadata.create_all(bind=database.engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with PostgreSQL!"}
