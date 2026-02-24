from .movie_genre import movie_genre
from .base import *

class Genre(BaseModel):
    __tablename__ = "genres"

    name = Column(String(50), unique=True, nullable=False)
    movies = db.relationship("Movie", secondary=movie_genre, back_populates="genres")

    def __str__(self):
        return self.name
