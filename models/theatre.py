from sqlalchemy import Column, Integer, String

from base.base import Base


class Theatre(Base):
    __tablename__ = 'theatre'
    theatre_id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
