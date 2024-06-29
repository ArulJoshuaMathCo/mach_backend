from uuid import UUID
from typing import List, Dict, Optional
from pydantic import BaseModel
from schemas.skills import SkillsBase

class ReplacementFinder(BaseModel):
    user_id: UUID
    name: str
    designation: Optional[str] = None
    account: Optional[str] = None
    lead: Optional[str] = None
    manager_name: Optional[str] = None
    skills: Dict[str,int]
    skills_count: int
    average_rating: float
    matching_skills: float

class ReplacementFinderResponse(BaseModel):
    skill_avg_ratings: Dict[str, float]
    overall_average_rating: float
    nearest_matches: List[ReplacementFinder]