from uuid import UUID
from typing import List, Optional, Dict
from pydantic import BaseModel
from schemas.skills import SkillsBase

class TalentFinder(BaseModel):
    user_id: UUID 
    name: str
    designation: Optional[str] = None
    account: Optional[str] = None
    lead: Optional[str] = None
    manager_name: Optional[str] = None
    skills_count: int
    average_rating: float
    skills: Dict[str, int]