from sqlalchemy import Column, Integer, String

from base.base import Base


class Genre(Base):
    __tablename__ = 'genre'
    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String)
