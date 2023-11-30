from sqlalchemy import Column, Integer, String, Float, ForeignKey

from base.base import Base


class Ticket(Base):
    __tablename__ = 'ticket'
    ticket_id = Column(Integer, primary_key=True)
    theatre_id = Column(Integer, ForeignKey('theatre.theatre_id'))
    performance_id = Column(Integer, ForeignKey('performance.performance_id'))
    play_id = Column(Integer, ForeignKey('play.play_id'))
    seat_number = Column(String)
    price = Column(Float)
    audience_member_id = Column(Integer, ForeignKey('audience_member.audience_member_id'))
