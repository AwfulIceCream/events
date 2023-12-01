from sqlalchemy import Column, Integer, String, Date, ForeignKey

from base.base import Base


class Performance(Base):
    __tablename__ = 'performance'
    performance_id = Column(Integer, primary_key=True)
    performance_date = Column(Date)
    duration = Column(Integer)
    time_start = Column(String)
    time_end = Column(String)
    theatre_id = Column(Integer, ForeignKey('theatre.theatre_id'))
    play_id = Column(Integer, ForeignKey('play.play_id'))
