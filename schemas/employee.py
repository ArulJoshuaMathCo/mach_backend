from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Json
from db.session import engine
from db.base_class import Base
Base.metadata.create_all(bind=engine)
from uuid import UUID

class EmployeeBase(BaseModel):
    name: str
    designation: str
    account: str
    lead: str
    manager_name: str
    latest:Optional[str] = None
    

class EmployeeCreate(EmployeeBase):
    user_id: UUID

class MACH_Employee(EmployeeBase):
    user_id: UUID

    class Config:
        orm_mode = True

class Employee1(MACH_Employee):
    class Config:
        orm_mode = True

