import enum
from .base import *
from flask_login import UserMixin

class RoleEnum(enum.Enum):
    Admin = "Admin"
    User = "User"

class Account(BaseModel, UserMixin):
    __tablename__ = "accounts"

    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.User)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    avatar_url = Column(String(255))
    is_pro = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    comments = db.relationship("Comment", backref="account", lazy=True, cascade="all, delete")

    def __str__(self):
        return f"<Account {self.username} - {self.role.value}>"

