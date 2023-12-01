from sqlalchemy import Column, Integer, ForeignKey

from base.base import Base


class PlayGenre(Base):
    __tablename__ = 'play_genre'
    play_genre_id = Column(Integer, primary_key=True)
    play_id = Column(Integer, ForeignKey('play.play_id'))
    genre_id = Column(Integer, ForeignKey('genre.genre_id'))
