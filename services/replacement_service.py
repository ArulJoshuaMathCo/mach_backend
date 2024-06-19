from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import func, or_
from concurrent.futures import ThreadPoolExecutor
import asyncio
from decimal import Decimal
from models.Employee import MACH_Employee as employeeModel
from models.skills import Skills1
from schemas.Employee_with_skills import SkillBase
from services.service import run_in_executor
async def map_skills_rf(filtered_skills: List[Skills1]) -> Dict:
    skills_map = {}
    for skill in filtered_skills:
        if skill.user_id not in skills_map:
            skills_map[skill.user_id] = []
        skills_map[skill.user_id].append(SkillBase(
            Python=skill.python,
            SQL=skill.sql,
            Excel=skill.excel,
            Storyboarding=skill.storyboarding,
            BusinessCommunication=skill.business_communication,
            Result_Orientation=skill.result_orientation,
            Quality_Focus=skill.quality_focus,
            Effective_Communication=skill.effective_communication,
            Work_Management_effectiveness=skill.work_management_and_effectiveness,
            ClientCentric=skill.clientcentric,
            GenAI=skill.genai,
            NucliOS=skill.nuclios
        ))
    return skills_map

async def fetch_employees_average(
    db: Session,
    user_ids: List[str]
) -> List[Any]:
    query = db.query(employeeModel).filter(employeeModel.user_id.in_(user_ids))
    return await run_in_executor(query.all)

async def calculate_skill_avg_ratings(
    db: Session,
    user_ids: List[str],
    skill_name: Optional[str]
) -> Dict[str, Decimal]:
    skill_avg_ratings = {}
    for skill_column in Skills1.__table__.columns:
        if skill_column.name != 'user_id':
            avg_rating_query = db.query(func.avg(skill_column)).filter(
                skill_column.isnot(None),
                Skills1.user_id.in_(user_ids)
            )
            if skill_name:
                avg_rating_query = avg_rating_query.filter(getattr(Skills1, skill_name.lower(), None).isnot(None))
            
            avg_rating = await run_in_executor(avg_rating_query.scalar)
            if avg_rating is not None:
                skill_avg_ratings[skill_column.name] = avg_rating
            else:
                skill_avg_ratings[skill_column.name] = Decimal(0)
    return skill_avg_ratings
async def calculate_overall_avg_rating(skill_avg_ratings: Dict[str, Decimal]) -> Decimal:
    return sum(skill_avg_ratings.values()) / len(skill_avg_ratings) if skill_avg_ratings else Decimal(0)

async def find_nearest_matches(
    employees_with_skills: List[Dict[str, Any]],
    overall_avg_rating: Decimal
) -> List[Dict[str, Any]]:
    nearest_matches = []
    for employee in employees_with_skills:
        if employee['average_rating'] >= overall_avg_rating:
            matching_skills = len(set(skill_name for skill in employee['skills'] for skill_name in skill.keys()))
            employee['matching_skills'] = matching_skills
            nearest_matches.append(employee)
    return nearest_matches