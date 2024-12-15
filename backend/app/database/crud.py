"""This module provides CRUD operations for the Hotel model in the database."""

from app.api.endpoints.logger import setup_logger
from app.database import models
from app.database.database import SessionLocal
from sqlalchemy.orm import Session

LOG = setup_logger("ta-ast-crud")


def get_db():
    """
    Provides a database session.

    **Yields:**
     - `SessionLocal`: A database session object.

    **Exceptions:**
        - `Exception`: If an error occurs while getting the database session, an exception is raised.
    """
    LOG.debug("Getting database session")
    db = SessionLocal()
    try:
        return db
    except Exception as exc:
        LOG.error("An error occurred while getting the database session")
        raise exc
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

    **Exceptions:**
        - `Exception`: If an error occurs while creating the hotel record, an exception is raised.
    """
    LOG.debug(f"Creating new hotel record for: {name}")

    try:
        db_hotel = models.Hotel(
            name=name, address=address, description=description, review=review
        )
        db.add(db_hotel)
        db.commit()
        db.refresh(db_hotel)

        LOG.debug(f"Hotel {name} created successfully")
        return db_hotel
    except:
        LOG.error(f"An error occurred while creating hotel: {name}")
        db.rollback()
        raise


def get_hotels_basic_info(db: Session):
    """
    Retrieve basic information for all hotels in the database.

    **Request Body:**
     - `db` (Session): The database session.

    **Returns:**
     - `List[models.Hotel]`: A list of hotel records containing basic information.

    **Exceptions:**
        - `Exception`: If an error occurs while getting hotel information, an exception is raised.
    """
    LOG.debug("Getting basic information for all hotels")

    try:
        hotels = db.query(models.Hotel).all()
    except Exception as exc:
        LOG.error("An error occurred while getting hotel information")
        raise exc

    if not hotels:
        LOG.warning("No hotels found")
        return None

    LOG.debug(f"Found {len(hotels)} hotels")
    return [{"name": hotel.name, "review": hotel.review} for hotel in hotels]


def get_hotel_by_id(db: Session, hotel_id: int):
    """
    Retrieve a specific hotel by its ID.

    **Request Body:**
        - `db` (Session): The database session.
        - `hotel_id` (int): The ID of the hotel to retrieve.

    **Returns:**
        - `models.Hotel`: The hotel record with the specified ID.

    **Exceptions:**
        - `Exception`: If an error occurs while retrieving the hotel record, an exception is raised.
    """
    LOG.debug(f"Getting hotel with ID: {hotel_id}")
    try:
        hotel = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()
    except Exception as exc:
        LOG.error(f"An error occurred while getting hotel with ID: {hotel_id}")
        raise exc

    if not hotel:
        LOG.warning(f"No hotel found with ID: {hotel_id}")
        return None

    LOG.debug(f"Found hotel: {hotel.name}")
    return hotel
