from sqlalchemy.orm import relationship

from app.models.base import Base
from sqlalchemy import TEXT, Column, UUID, DateTime, ForeignKey, Integer, String, text


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"),nullable=False)
    status = Column(String(50), nullable=False, default="PENDING")
    attempt_count = Column(Integer, nullable=False, default=0)
    validation_errors = Column(TEXT, nullable=True)
    email_status = Column(String(50), nullable=False, default="PENDING")
    workflow_type = Column(String(50), nullable=False, default="NEW_REGISTRATION")
    
    started_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=True)
    completed_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=True)

    #Relationships
    customer = relationship("Customer", back_populates="workflow_runs")