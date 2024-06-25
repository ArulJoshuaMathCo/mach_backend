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
# async def map_skills_rf(filtered_skills: List[Skills1]) -> Dict:
#     skills_map = {}
#     for skill in filtered_skills:
#         if skill.user_id not in skills_map:
#             skills_map[skill.user_id] = []
#         skills_map[skill.user_id].append(SkillBase(
#             Python=skill.python,
#             SQL=skill.sql,
#             Excel=skill.excel,
#             Storyboarding=skill.storyboarding,
#             BusinessCommunication=skill.business_communication,
#             Result_Orientation=skill.result_orientation,
#             Quality_Focus=skill.quality_focus,
#             Effective_Communication=skill.effective_communication,
#             Work_Management_effectiveness=skill.work_management_and_effectiveness,
#             ClientCentric=skill.clientcentric,
#             GenAI=skill.genai,
#             NucliOS=skill.nuclios
#         ))
#     return skills_map

# async def fetch_employees_average(
#     db: Session,
#     user_ids: List[str]
# ) -> List[Any]:
#     query = db.query(employeeModel).filter(employeeModel.user_id.in_(user_ids))
#     return await run_in_executor(query.all)

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
                skill_avg_ratings[skill_column.name] = float(0)
    return skill_avg_ratings
# async def calculate_overall_avg_rating(skill_avg_ratings: Dict[str, float]) -> float:
#     return sum(skill_avg_ratings.values()) / len(skill_avg_ratings) if skill_avg_ratings else float(0)

# async def find_nearest_matches(
#     employees_with_skills: List[Dict[str, Any]],
#     overall_avg_rating: Decimal
# ) -> List[Dict[str, Any]]:
#     nearest_matches = []
#     for employee in employees_with_skills:
#         if employee['average_rating'] >= overall_avg_rating:
#             matching_skills = len(set(skill_name for skill in employee['skills'] for skill_name in skill.keys()))
#             employee['matching_skills'] = matching_skills
#             nearest_matches.append(employee)
#     return nearest_matches
async def process_employees_with_skills(
    employees: List[employeeModel],
    skills_map: Dict[str, List[Skills1]]
) -> List[Dict[str, Any]]:
    employees_with_skills = []
    for employee in employees:
        employee_skills = skills_map.get(employee.user_id, [])
        filtered_skills = [
            {k: v for k, v in skill.__dict__.items() if v is not None and v > 0 and k != '_sa_instance_state'} for skill in employee_skills
        ]
        total_skills_rated = sum(len(skill) for skill in filtered_skills)
        total_rating = sum(value for skill in filtered_skills for value in skill.values())
        average_rating = (total_rating / total_skills_rated) if total_skills_rated > 0 else 0
        
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
# async def calculate_skill_avg_ratings(db: Session, user_ids: List[str]) -> Dict[str, float]:
#     skill_avg_ratings = {}
#     skills_query = select(Skills1).where(Skills1.user_id.in_(user_ids))
#     skills_result =  db.execute(skills_query)
#     skills = skills_result.scalars().all()

#     skill_totals = {}
#     skill_counts = {}

#     # Define the list of skill attributes to check
#     skill_attributes = [column.name for column in Skills1.__table__.columns if column.name != 'user_id']

#     for skill in skills:
#         for skill_name in skill_attributes:
#             skill_value = getattr(skill, skill_name.lower(), None)
#             if skill_value is not None:
#                 if skill_name not in skill_totals:
#                     skill_totals[skill_name] = 0
#                     skill_counts[skill_name] = 0
#                 skill_totals[skill_name] += skill_value
#                 skill_counts[skill_name] += 1

#     for skill_name in skill_totals.keys():
#         skill_avg_ratings[skill_name] = skill_totals[skill_name] / skill_counts[skill_name]

#     return skill_avg_ratings


async def calculate_overall_avg_rating(skill_avg_ratings: Dict[str, float]) -> float:
    total_rating = sum(skill_avg_ratings.values())
    total_skills = len(skill_avg_ratings)
    return total_rating / total_skills if total_skills > 0 else 0

async def find_nearest_matches(employees_with_skills: List[Dict[str, Any]], overall_avg_rating: float,page: int=1,
    page_size: int=5) -> List[Dict[str, Any]]:
    # Example implementation for finding nearest matches based on average rating
    employees_with_skills.sort(key=lambda x: abs(x['average_rating'] - overall_avg_rating))
    # start_index = (page - 1) * page_size
    # end_index = start_index + page_size

    return employees_with_skills[:]  # Return top 5 nearest matches
