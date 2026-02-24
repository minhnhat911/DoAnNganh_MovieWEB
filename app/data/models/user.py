from .base import *


class User(BaseModel):
    __tablename__ = "users"

    first_name = Column(String(50),nullable=False)
    last_name = Column(String(50),nullable=False)
    gender = Column(String(10))
    date_of_birth = Column(DateTime)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    created_at = Column(DateTime,default=datetime.now())

    account = relationship("Account", backref="user", uselist=False, lazy='joined',cascade="all, delete")

    @property
    def user_code(self):
        return f"U{self.id:03d}"

    def __str__(self):
        return self.user_code

