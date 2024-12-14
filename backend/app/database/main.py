"""Main module for FastAPI application with PostgreSQL database integration."""

from app.database import database, models
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
def startup():
    """
    Initialize the database by creating all tables defined in the models.
    """

    models.Base.metadata.create_all(bind=database.engine)


@app.get("/")
def read_root():
    """
    Handle the root endpoint and return a welcome message.
    Returns:
        dict: A dictionary containing a welcome message.
    """

    return {"message": "Welcome to FastAPI with PostgreSQL!"}
