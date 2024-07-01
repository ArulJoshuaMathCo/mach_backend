from sqlalchemy import Column, Integer, String, ForeignKey
import uuid
from sqlalchemy.dialects.postgresql import UUID
from db.base_class import Base
from db.session import engine
Base.metadata.create_all(bind=engine)
from sqlalchemy.orm import relationship,column_property
from models.user import User
from models.skills import Skills1


class MACH_Employee(Base):
    user_id = column_property(Column("EMP ID", String, primary_key=True, default=uuid.uuid4, index=True))
    name = Column(String, index=True)
    designation = column_property(Column("Designation", String)) 
    account = Column(String)
    lead = column_property(Column("Lead", String))
    manager_name = column_property(Column("Manager", String))
    validation = column_property(Column("Validation", String))
    tenure = column_property(Column("Tenure_Buckets", String))
    iteration=column_property(Column("iteration", Integer))
    capabilities = column_property(Column("capabilities", String))
    serviceline_name = column_property(Column("serviceline_name", String))
    function = column_property(Column("Function", String))
    submitted_by = column_property(Column("submitted_by", String,ForeignKey("user.role"), nullable=True))
    skills = relationship("Skills1", back_populates="employee")
    submitter= relationship("User", back_populates="employees")