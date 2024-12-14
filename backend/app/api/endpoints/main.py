"""
Main FastAPI application setup with CORS middleware and database initialization.
"""

from app.api.endpoints.hotels import router
from app.api.endpoints.logger import setup_logger
from app.database import database, models
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

LOG = setup_logger("ta-ast-main")


@app.on_event("startup")
def startup() -> None:
    """
    Initializes the database by creating all tables defined in the models.
    """
    LOG.debug("Creating all tables in the database")
    models.Base.metadata.create_all(bind=database.engine)


@app.get("/")
def read_root() -> dict:
    """
    Handle the root endpoint and return a welcome message.

    **Returns:**
        dict: A dictionary containing a welcome message.
    """

    return {"message": "Welcome to FastAPI with PostgreSQL!"}
