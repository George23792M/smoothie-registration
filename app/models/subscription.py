from sqlalchemy import UUID, Column, Date, ForeignKey, String, text
from sqlalchemy.orm import relationship

from app.models.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    plan_name = Column(String(100), nullable=False, default = "Basic - Standard Smoothie Plan")
    status = Column(String(50), nullable=False, default="ACTIVE")
    start_date = Column(Date, server_default=text("CURRENT_DATE"), nullable=False)
    end_date = Column(Date, nullable=False)
    cre_ts = Column(String, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updt_ts = Column(String, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"), nullable=True)
    
    #Relationships:(Many-To-One) A subscription belongs to a single customer
    customer = relationship("Customer", back_populates="subscriptions")