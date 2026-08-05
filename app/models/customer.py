from sqlalchemy import UUID, Boolean, Column, String, text
from sqlalchemy.orm import relationship
from app.models.base import Base
    

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False)
    preferred_name = Column(String(100))
    email = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    cre_ts = Column(String, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updt_ts = Column(String, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"), nullable=True)
    
    #Relationships:(One-To-Many) A customer can have multiple smoothiee subscriptions
    subscriptions = relationship("Subscription", back_populates="customer", cascade="all, delete-orphan")
    preferences = relationship("CustomerPreference", back_populates="customer", cascade="all, delete-orphan")