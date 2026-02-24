from . import movie_actor
from .base import *

class Actor(BaseModel):
    __tablename__ = "actors"

    name = Column(String(100), nullable=False)
    description = Column(Text)
    date_of_birth = Column(DateTime)
    avatar_url = Column(String(255))

    movies = db.relationship("Movie", secondary=movie_actor, back_populates="actors")

    def __str__(self):
        return self.name
