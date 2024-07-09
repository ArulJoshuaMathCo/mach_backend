from typing import List, Optional
from pydantic import BaseModel

class RatingPercentage(BaseModel):
    rating: int
    number_of_employees: int
    percentage: float

class SkillPercentage(BaseModel):
    skill: str
    number_of_employees: int
    percentage: float
    average_rating: Optional[float]
    rating_percentages: List[RatingPercentage]

class ServiceLineSkill(BaseModel):
    serviceline_name: str
    number_of_employees: int
    employee_percentage: float
    average_rating: Optional[float]
    skill_percentages: List[SkillPercentage]

class EmployeeSkill(BaseModel):
    skill_name: str
    average_rating: Optional[float] = None
    employee_count: int

class EmployeeSkillScreen(BaseModel):
    overall_average: float
    number_of_people: int
    skill_avg_ratings: List[EmployeeSkill]

class ExecutiveSummary(BaseModel):
    service_line_skill_percentages: List[ServiceLineSkill]
    overall_average: float
    number_of_people: int
    skill_avg_ratings: List[EmployeeSkill]