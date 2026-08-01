from sqlalchemy import UUID, Boolean, Column, Date, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from app.models.preference import Base, relationship

    
class CustomerPreference(Base):
    __tablename__ = "customer_preferences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    profile_name = Column(String(100), nullable=False, default = "Default Profile")
    days = Column(Integer, nullable=False, default=7) 
    max_calories = Column(Integer, nullable=False, default=500)
    nut_free = Column(Boolean,  default=False)
    gluten_free = Column(Boolean,  default=False)
    dairy_free = Column(Boolean,  default=False)
    soy_free = Column(Boolean,  default=False)
    cre_ts = Column(String, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updt_ts = Column(String, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"), nullable=True)    

    customer = relationship("Customer", back_populates="preferences")