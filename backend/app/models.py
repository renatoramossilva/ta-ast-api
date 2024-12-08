from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    review = Column(Float, nullable=False)

    def __repr__(self):
        return f'<Hotel {self.name}>'
