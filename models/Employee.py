from sqlalchemy import Column, Integer, String, ForeignKey
import uuid
from sqlalchemy.dialects.postgresql import UUID
from db.base_class import Base
from sqlalchemy.orm import relationship


class MACH_Employee(Base):
    # __tablename__ = "Employee_Data"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True)
    designation = Column(String)
    account = Column(String)
    lead = Column(String)
    manager_name = Column(String)
    # skills = relationship("Skill", back_populates="employee")
    