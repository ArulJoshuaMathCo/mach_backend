from typing import List
from pydantic import BaseModel

class DesignationCount(BaseModel):
    designation: str
    count: int

class DesignationCounts(BaseModel):
    designation_counts: List[DesignationCount]
    total_count: int