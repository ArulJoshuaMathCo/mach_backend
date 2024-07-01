from typing import List, Optional
from pydantic import BaseModel

class EmployeeSkill(BaseModel):
    skill_name: str
    average_rating: Optional[float] = None
    employee_count: int

class EmployeeSkillScreen(BaseModel):
    overall_average: float
    number_of_people: int
    skill_avg_ratings: List[EmployeeSkill]