from .base import *

class WatchHistory(BaseModel):
    __tablename__ = "watch_history"

    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    episode_id = Column(Integer, ForeignKey("episodes.id"), nullable=False)
    progress = Column(Integer, default=0)   # phút đã xem
    last_watched = Column(DateTime, default=datetime.now())

    def __str__(self):
        return f"<WatchHistory account_id={self.account_id} episode_id={self.episode_id}>"
