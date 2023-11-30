from sqlalchemy import Column, Integer, String

from base.base import Base


class Language(Base):
    __tablename__ = 'language'
    language_id = Column(Integer, primary_key=True)
    name = Column(String)
