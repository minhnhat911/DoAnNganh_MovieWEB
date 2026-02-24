from .base import *
from sqlalchemy import DECIMAL

class Subscription(BaseModel):
    __tablename__ = "subscriptions"

    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    plan_name = Column(String(50), nullable=False)  # VIP, Premium...
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    price = Column(DECIMAL(10,2))

    def __str__(self):
        return f"<Subscription {self.plan_name} {self.start_date} - {self.end_date}>"
