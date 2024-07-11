from typing import List, Optional
from pydantic import BaseModel

class Rating(BaseModel):
    rating: int
    percentage: float
    employee_count: int

class SkillAvgRating(BaseModel):
    skill_name: str
    average_rating: float
    employee_count: int
    rating_details: List[Rating]

class OverallSkillRatings(BaseModel):
    overall_average: float
    number_of_people: int
    skill_avg_ratings: List[SkillAvgRating]

    class Config:
        orm_mode = True