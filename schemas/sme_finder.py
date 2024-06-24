from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel
from schemas.Employee_with_skills import SkillBase

class SmeFinder(BaseModel):
    user_id:UUID 
    name: str
    designation: str
    account: str
    lead: str
    manager_name: str
    validated: Optional[str] = None
    skills: List[SkillBase]