from uuid import UUID
from typing import List, Dict, Optional
from pydantic import BaseModel
from schemas.skills import SkillsBase

class ReplacementFinder(BaseModel):
    user_id: str
    name: str
    designation: Optional[str] = None
    account: Optional[str] = None
    lead: Optional[str] = None
    manager_name: Optional[str] = None
    tenure: Optional[str] = None
    iteration: Optional[int] = None
    capabilities: Optional[str] = None
    serviceline_name: Optional[str] = None
    functions: Optional[str] = None
    skills_count: int
    average_rating: float
    skills: Dict[str, int]
    matching_skills: float
    matched_skills:Dict[str, int]

class ReplacementFinderResponse(BaseModel):
    skill_avg_ratings: Dict[str, float]
    overall_average_rating: float
    nearest_matches: List[ReplacementFinder]