from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional,Sequence
from pydantic import BaseModel, Json
# from db.session import engine
from db.base_class import Base
# Base.metadata.create_all(bind=engine)
from uuid import UUID

class EmployeeBase(BaseModel):
    name: str
    designation: Optional[str] = None
    account: Optional[str] = None
    lead: Optional[str] = None
    manager_name: Optional[str] = None
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

class employeeSearchResults(BaseModel):
    results: Sequence[MACH_Employee]

