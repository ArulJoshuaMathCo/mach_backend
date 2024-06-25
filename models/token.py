from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base_class import Base
from db.session import engine
import datetime
# Base.metadata.create_all(bind=engine)
class TokenData(Base):
    id = Column(Integer, index=True)
    token = Column(String, primary_key=True, nullable=False, unique=True)
    refresh_token = Column(String, nullable=False, unique=True)
    created_date = Column(DateTime, default=datetime.datetime.now)
    is_active = Column(Boolean, default=True)