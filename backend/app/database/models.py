"""This module defines the SQLAlchemy ORM model for the Hotel entity."""

from typing import Any

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base: Any = declarative_base()


class Hotel(Base):  # pylint: disable=too-few-public-methods
    """SQLAlchemy ORM model for the Hotel entity."""

    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    description = Column(String)
    review = Column(Float)

    def __repr__(self):
        return (
            f"<Hotel(name={self.name}, address={self.address}, "
            f"description={self.description}, review={self.review})>"
        )
