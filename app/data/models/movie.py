from .movie_genre import movie_genre
from .movie_actor import movie_actor
from .base import *
from sqlalchemy import Numeric


class Movie(BaseModel):
    __tablename__ = "movies"

    title = Column(String(255), nullable=False)
    description = Column(Text)
    release_year = Column(Integer)
    duration = Column(Integer)   # phút
    rating = Column(Numeric(2, 1), default=0)  # 1-5 sao
    poster_url = Column(String(255))
    trailer_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    is_pro = Column(Boolean, default=False)


    #Quan he n-n
    genres = db.relationship("Genre", secondary=movie_genre, back_populates="movies")
    actors = db.relationship("Actor", secondary=movie_actor, back_populates="movies")
    # Quan hệ 1-n
    episodes = db.relationship("Episode", backref="movie", lazy=True, cascade="all, delete")
    comments = db.relationship("Comment", backref="movie", lazy=True, cascade="all, delete")

    def __str__(self):
        return self.title
