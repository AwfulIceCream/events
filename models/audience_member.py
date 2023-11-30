from sqlalchemy import Column, Integer, String, Date

from base.base import Base


class AudienceMember(Base):
    __tablename__ = 'audience_member'
    audience_member_id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password = Column(String)
    birthdate = Column(Date)
    name = Column(String)
    surname = Column(String)
    middle_name = Column(String, nullable=True)
