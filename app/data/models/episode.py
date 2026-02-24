from .base import *

class Episode(BaseModel):
    __tablename__ = "episodes"

    title = Column(String(255))
    episode_number = Column(Integer)
    video_url = Column(String(255), nullable=False)
    likes = Column(Integer, default = 0)
    views = Column(Integer, default=0)

    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)

    watch_histories = db.relationship("WatchHistory", backref="episode", lazy=True, cascade="all, delete")

    def __str__(self):
        return f"<Episode {self.episode_number} - {self.title}>"
