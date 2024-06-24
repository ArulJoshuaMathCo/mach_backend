from uuid import UUID
from typing import List, Dict, Optional
from pydantic import BaseModel
from schemas.skills import SkillsBase

class ReplacementFinder(BaseModel):
    user_id: UUID
    name: str
    designation: str
    account: str
    lead: str
    manager_name: str
    validated: Optional[str] = None
    skills: List[SkillsBase]
    total_skills_rated: float
    average_rating: float
    matching_skills: float

class ReplacementFinderResponse(BaseModel):
    skill_avg_ratings: Dict[str, float]
    overall_average_rating: float
    nearest_matches: List[ReplacementFinder]