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
from sqlalchemy.ext.asyncio import AsyncSession

async def run_in_executor(db_func, *args):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, db_func, *args)

async def fetch_employees(
    db: AsyncSession,
    name: Optional[str],
    designation: Optional[str],
    account: Optional[str],
    lead: Optional[str],
    manager_name: Optional[str] = None,
    validated: Optional[str] = None
) -> List[Any]:
    query = db.query(employeeModel)
    if name:
        query = query.filter(employeeModel.name == name)
    if designation:
        query = query.filter(employeeModel.designation == designation)
    if account:
        query = query.filter(employeeModel.account == account)
    if lead:
        query = query.filter(employeeModel.lead == lead)
    if manager_name:
        query = query.filter(employeeModel.manager_name == manager_name)
    if validated:
        query = query.filter(employeeModel.latest == validated)
    return await run_in_executor(query.all)

async def fetch_skills(
    db: AsyncSession,
    skill_name: Optional[str],
    rating: Optional[int]
) -> List[Any]:
    query = db.query(Skills1)
    if skill_name:
        skill_column = getattr(Skills1, skill_name.lower(), None)
        if skill_column is not None:
            if rating is not None:
                query = query.filter(skill_column == rating)
            else:
                query = query.filter(skill_column.isnot(None))
    elif rating is not None:
        or_conditions = []
        for column in Skills1.__table__.columns:
            if column.name != 'user_id':  # Exclude user_id column from filtering
                or_conditions.append(column == rating)
        query = query.filter(or_(*or_conditions))
    return await run_in_executor(query.all)

async def map_skills(filtered_skills: List[Skills1]) -> Dict:
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
    db: AsyncSession,
    user_ids: List[str]
) -> List[Any]:
    query = db.query(employeeModel).filter(employeeModel.user_id.in_(user_ids))
    return await run_in_executor(query.all)

async def calculate_skill_avg_ratings(
    db: AsyncSession,
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

async def process_employees_with_skills(
    employees: List[employeeModel],
    skills_map: Dict[str, List[SkillBase]]
) -> List[Dict[str, Any]]:
    employees_with_skills = []
    for employee in employees:
        employee_skills = skills_map.get(employee.user_id, [])
        filtered_skills = [
            {k: v for k, v in skill.dict().items() if v is not None and v > 0} for skill in employee_skills
        ]
        total_skills_rated = sum(len(skill) for skill in filtered_skills)
        average_rating = (sum(
            value for skill in filtered_skills for value in skill.values()
        ) / total_skills_rated) if total_skills_rated > 0 else 0
        employees_with_skills.append({
            "user_id": employee.user_id,
            "name": employee.name,
            "designation": employee.designation,
            "account": employee.account,
            "lead": employee.lead,
            "manager_name": employee.manager_name,
            "validated": employee.latest,
            "skills": filtered_skills,
            "total_skills_rated": total_skills_rated,
            "average_rating": average_rating
        })
    return employees_with_skills

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

async def fetch_employees_by_user_ids(
    db: AsyncSession,
    user_ids: List[str]
) -> List[Any]:
    query = db.query(employeeModel).filter(employeeModel.user_id.in_(user_ids))
    return await run_in_executor(query.all)
