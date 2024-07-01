from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, column_property
from db.base_class import Base
class Skills1(Base):
    user_id=column_property(Column("EMP ID", String, ForeignKey('mach_employee.EMP ID'), primary_key=True)) 
    python = column_property(Column("Python", Integer, nullable=True))     
    sql = column_property(Column("SQL", Integer, nullable=True))     
    excel = column_property(Column("Excel", Integer, nullable=True))     
    storyboarding = column_property(Column("Storyboarding", Integer, nullable=True))     
    business_communication = column_property(Column("Business Communication", Integer, nullable=True)) 
    exploratory_data_analysis = column_property(Column("Exploratory Data Analysis", Integer, nullable=True))    
    statistics = column_property(Column("Statistics", Integer, nullable=True))              
    probability = column_property(Column("Probability", Integer, nullable=True))        
    regression = column_property(Column("Regression", Integer, nullable=True))     
    clustering = column_property(Column("Clustering", Integer, nullable=True))   
    neural_networks = column_property(Column("Neural Networks", Integer, nullable=True))     
    reinforcement_learning = column_property(Column("Reinforcement Learning", Integer, nullable=True))   
    tableau = column_property(Column("Tableau", Integer, nullable=True))    
    powerbi = column_property(Column("PowerBi", Integer, nullable=True))    
    aws = column_property(Column("AWS", Integer, nullable=True))     
    azure = column_property(Column("Azure", Integer, nullable=True))  
    employee = relationship("MACH_Employee", back_populates="skills")