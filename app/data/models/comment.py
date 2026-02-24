from .base import *

class Comment(BaseModel):
    __tablename__ = "comments"

    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    review = Column(Text)
    created_at = Column(DateTime, default=datetime.now())

    def __str__(self):
        return f"<Comment {self.review} stars>"
