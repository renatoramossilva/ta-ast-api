from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def create_hotel(name: str, address: str, description: str, review: float, db: Session):
    db_hotel = models.Hotel(
        name=name, address=address, description=description, review=review
    )
    print(db_hotel)
    print(db)
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel
