from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship
from db.session import engine
from db.base_class import Base
# Base.metadata.create_all(bind=engine)

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    surname = Column(String(256), nullable=True)
    email = Column(String, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    # employees = relationship(
    #     "Employee",
    #     cascade="all,delete-orphan",
    #     back_populates="submitter",
    #     uselist=True,
    # )
    hashed_password = Column(String, nullable=False)