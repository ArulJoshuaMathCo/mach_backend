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

from typing import List, Optional
from pydantic import BaseModel, Field

class RatingDetail(BaseModel):
    rating: int
    count_of_employees: int
    percentage_of_rating: float

class SkillAverageRating(BaseModel):
    skill: str
    employee_count: int
    percentage: float
    skill_average_rating: float
    rating_percentages: List[RatingDetail]

class Rating(BaseModel):
    rating: int
    percentage: float
    employee_count: int

class SkillAverage(BaseModel):
    skill_name: str
    average_rating: float
    employee_count: int
    rating_details: List[Rating]

class ServiceLineSkillPercentage(BaseModel):
    serviceline_name: str
    number_of_employees: int
    employee_percentage: float
    average_rating: float
    skill_percentages: List[SkillAverageRating]

class ServiceLinePercentage(BaseModel):
    serviceline: str
    employees: int
    percentage_of_employees: float
    average_rating_of_serviceline: float

class ResponseData(BaseModel):
    service_line_percentage: List[ServiceLinePercentage]
    service_line_skill_percentages: List[ServiceLineSkillPercentage]
    overall_average: float
    total_number_of_people: int
    skill_avg_ratings: List[SkillAverage]