"""This module provides CRUD operations for the Hotel model in the database."""

from app.database import models
from app.database.database import SessionLocal
from sqlalchemy.orm import Session


def get_db():
    """
    Provides a database session.

    **Yields:**
     - `SessionLocal`: A database session object.
    """

    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def create_hotel(name: str, address: str, description: str, review: float, db: Session):
    """
    Create a new hotel record in the database.

    **Request Body:**
     - `name` (str): The name of the hotel.
     - `address` (str): The address of the hotel.
     - `description` (str): A brief description of the hotel.
     - `review` (float): The review rating of the hotel.
     - `db` (Session): The database session.

    **Returns:**
     - `models.Hotel`: The newly created hotel record.
    """

    db_hotel = models.Hotel(
        name=name, address=address, description=description, review=review
    )
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel
