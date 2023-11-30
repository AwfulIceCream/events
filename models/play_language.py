from sqlalchemy import Column, Integer, ForeignKey

from base.base import Base


class PlayLanguage(Base):
    __tablename__ = 'play_language'
    play_language_id = Column(Integer, primary_key=True)
    play_language_play = Column(Integer, ForeignKey('play.play_id'))
    language_play_language = Column(Integer, ForeignKey('language.language_id'))
