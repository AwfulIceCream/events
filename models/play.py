from sqlalchemy import Column, Integer, String

from base.base import Base


class Play(Base):
    __tablename__ = 'play'
    play_id = Column(Integer, primary_key=True)
    name = Column(String)
    duration = Column(Integer)
    constraints = Column(Integer)
    rating = Column(Integer, nullable=True)
