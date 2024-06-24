from sqlalchemy import Column, Integer, String, ForeignKey
import uuid
from sqlalchemy.dialects.postgresql import UUID
from db.base_class import Base
from db.session import engine
# Base.metadata.create_all(bind=engine)
from sqlalchemy.orm import relationship
from models.user import User
from models.skills import Skills1


class MACH_Employee(Base):
    # __tablename__ = "Employee_Data"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True)
    designation = Column(String)
    account = Column(String)
    lead = Column(String)
    manager_name = Column(String)
    latest = Column(String)
    submitter_id = Column(Integer, ForeignKey("user.id"), nullable=True, default=1) 
    skills = relationship("Skills1", back_populates="employee")
    submitter= relationship("User", back_populates="employees")
    