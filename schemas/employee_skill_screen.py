from typing import List, Optional
from pydantic import BaseModel

class SkillAvgRating(BaseModel):
    skill_name: str
    average_rating: Optional[float] = None
    employee_count: int

class OverallSkillRatings(BaseModel):
    overall_average: float
    number_of_people: int
    skill_avg_ratings: List[SkillAvgRating]

    class Config:
        orm_mode = True