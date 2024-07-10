from typing import Optional
from pydantic import BaseModel, Field
from db.session import engine
from db.base_class import Base
# Base.metadata.create_all(bind=engine)
from uuid import UUID

class SkillsBase(BaseModel):
    user_id:str
    Python: Optional[int] = None
    SQL: Optional[int] = None
    Excel: Optional[int] = None
    Storyboarding: Optional[int] = None
    business_communication: Optional[int] = Field(None, alias="Business Communication")
    exploratory_data_analysis: Optional[int] = Field(None, alias="Exploratory Data Analysis")
    Statistics: Optional[int] = None
    Probability: Optional[int] = None
    Regression: Optional[int] = None
    Clustering: Optional[int] = None
    neural_networks: Optional[int] = Field(None, alias="Neural Networks")
    reinforcement_learning: Optional[int] = Field(None, alias="Reinforcement Learning")
    Tableau: Optional[int] = None
    PowerBi: Optional[int] = None
    AWS: Optional[int] = None
    Azure: Optional[int] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True