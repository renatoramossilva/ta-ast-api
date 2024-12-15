"""This module defines the SQLAlchemy ORM model for the Hotel entity."""

from typing import Any

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base: Any = declarative_base()


class Hotel(Base):  # pylint: disable=too-few-public-methods
    """SQLAlchemy ORM model for the Hotel entity."""

    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    description = Column(String)
    review = Column(Float)

    amenities = relationship(
        "Amenity", back_populates="hotel", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Hotel(name={self.name}, address={self.address}, "
            f"description={self.description}, review={self.review})>"
        )


class Amenity(Base):
    __tablename__ = "amenities"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)

    hotel = relationship("Hotel", back_populates="amenities")

    def __repr__(self):
        return f"<Amenity(name={self.name})>"
