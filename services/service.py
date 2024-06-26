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
    name: Optional[List[str]]=None,
    designation: Optional[List[str]]= None,
    account: Optional[List[str]]= None,
    lead: Optional[List[str]]= None,
    manager_name: Optional[List[str]]= None,
    validated: Optional[List[str]]= None,
    skill_name: Optional[List[str]]= None,
    rating: Optional[List[int]]= None,
    # page: int=1, page_size: int=10
) -> List[employeeModel]:
    query = select(employeeModel).join(Skills1, employeeModel.user_id == Skills1.user_id)

    if name:
        query = query.where(employeeModel.name.in_(name))
    if designation:
        query = query.where(employeeModel.designation.in_(designation))
    if account:
        query = query.where(employeeModel.account.in_(account))
    if lead:
        query = query.where(employeeModel.lead.in_(lead))
    if manager_name:
        query = query.where(employeeModel.manager_name.in_(manager_name))
    if validated:
        query = query.where(employeeModel.latest.in_(validated))
    if skill_name:
        # Create OR conditions for skill names
        skill_conditions = [getattr(Skills1, skill.lower(), None).isnot(None) for skill in skill_name if getattr(Skills1, skill.lower(), None) is not None]
        if skill_conditions:
            query = query.where(or_(*skill_conditions))
    if rating is not None:
        # Construct OR condition for all columns of Skills1
        or_conditions = []
        for column in Skills1.__table__.columns:
            if column.name != 'user_id':  # Exclude user_id column from filtering
                for rate in rating:
                    or_conditions.append(column == rate)
        
        # Apply the OR conditions to the query
        query = query.filter(or_(*or_conditions))
    
    result = db.execute(query)
    return result.scalars().all()

def paginate(query, page: int, page_size: int):
    return query.offset((page - 1) * page_size).limit(page_size)

# async def fetch_employees(
#     db: AsyncSession,
#     name: Optional[str] = None,
#     designation: Optional[str]= None,
#     account: Optional[str]= None,
#     lead: Optional[str]= None,
#     manager_name: Optional[str] = None,
#     validated: Optional[str] = None,
#     offset: int = 0,  # default offset is 0
#     limit: int = 100
# ) -> List[Any]:
#     query = db.query(employeeModel)
#     if name:
#         query = query.filter(employeeModel.name == name)
#     if designation:
#         query = query.filter(employeeModel.designation == designation)
#     if account:
#         query = query.filter(employeeModel.account == account)
#     if lead:
#         query = query.filter(employeeModel.lead == lead)
#     if manager_name:
#         query = query.filter(employeeModel.manager_name == manager_name)
#     if validated:
#         query = query.filter(employeeModel.latest == validated)
#     query = query.offset(offset).limit(limit)
#     return await run_in_executor(query.all)

async def fetch_skills(
    db: AsyncSession,
    skill_name: Optional[str],
    rating: Optional[int],
    offset: int = 0,  # default offset is 0
    limit: int = 100
) -> List[Any]:
    skills_query = db.query(Skills1)

    if skill_name is not None and rating is not None:
        # Assuming skills are filtered based on the lowercase version of their names
        skill_column = getattr(Skills1, skill_name.lower(), None)
        if skill_column is not None:
            skills_query = skills_query.filter(skill_column == rating)
    if skill_name is not None and rating is None:
        skill_column = getattr(Skills1,skill_name.lower(),None)
        if skill_column is not None:
            skills_query = skills_query.filter(skill_column.isnot(None))
    if skill_name is None and rating is not None:
        # Construct OR condition for all columns of Skills1
        or_conditions = []
        for column in Skills1.__table__.columns:
            if column.name != 'user_id':  # Exclude user_id column from filtering
                or_conditions.append(column == rating)
        
        # Apply the OR conditions to the query
        skills_query = skills_query.filter(or_(*or_conditions))
    skills_query = skills_query
    return await run_in_executor(skills_query.all)

async def map_skills(filtered_skills: List[Skills1],skill_name:Optional[str], rating:Optional[int]) -> Dict:
    skills_map = {}
    for skill in filtered_skills:
        skill_data = {}
        if skill.python is not None and (skill_name == 'python' or skill_name is None) and (rating is None or skill.python == rating):
            skill_data['Python'] = skill.python
        if skill.sql is not None and (skill_name == 'sql' or skill_name is None) and (rating is None or skill.sql == rating):
            skill_data['SQL'] = skill.sql
        if skill.excel is not None and (skill_name == 'excel' or skill_name is None) and (rating is None or skill.excel == rating):
            skill_data['Excel'] = skill.excel
        if skill.storyboarding is not None and (skill_name == 'storyboarding' or skill_name is None) and (rating is None or skill.storyboarding == rating):
            skill_data['Storyboarding'] = skill.storyboarding
        if skill.business_communication is not None and (skill_name == 'business_communication' or skill_name is None) and (rating is None or skill.business_communication == rating):
            skill_data['BusinessCommunication'] = skill.business_communication
        if skill.genai is not None and (skill_name == 'genai' or skill_name is None) and (rating is None or skill.genai == rating):
            skill_data['GenAI'] = skill.genai
        if skill.nuclios is not None and (skill_name == 'nuclios' or skill_name is None) and (rating is None or skill.nuclios == rating):
            skill_data['NucliOS'] = skill.nuclios

        if skill.user_id not in skills_map:
            skills_map[skill.user_id] = []
        skills_map[skill.user_id].append(SkillBase(**skill_data))
    return skills_map


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


async def process_employees_with_skills1(
    employees: List[employeeModel],
    rating:Optional[List[int]]=None,
    skill_query_name:Optional[List[str]]= None
) -> List[Dict[str, Any]]:
    employees_with_skills = []
    for employee in employees:
        total_skills_rated = 0
        total_rating = 0
        skills_data = {}

        # Ensure employee.skills is loaded and not empty
        if employee.skills:
            # Iterate over the attributes of the skills object
            for skill in employee.skills:
                for skill_name, skill_value in skill.__dict__.items():
                    if skill_name != 'user_id' and skill_name != '_sa_instance_state' and isinstance(skill_value, (int, float)):  # Exclude user_id column
                        total_skills_rated += 1
                        total_rating += skill_value
                        if rating and skill_query_name is not None:
                            for skill in skill_query_name:
                                for rate in rating:
                                    if rate is None or rate==skill_value and skill is None or skill == skill_name:
                                        skills_data[skill_name] = skill_value
                        elif rating is not None and skill_query_name is None:
                            for rate in rating:
                                if rate is None or rate==skill_value:
                                    skills_data[skill_name] = skill_value
                        elif skill_query_name is not None and rating is None:
                            for skill in skill_query_name:
                                if skill is None or skill == skill_name:
                                    skills_data[skill_name] = skill_value
                        else:
                            if rating is None and skill_query_name is None:
                                skills_data[skill_name] = skill_value

            average_rating = (total_rating / total_skills_rated) if total_skills_rated > 0 else 0
        else:
            average_rating = 0

        employees_with_skills.append({
            "user_id": employee.user_id,
            "name": employee.name,
            "designation": employee.designation,
            "account": employee.account,
            "lead": employee.lead,
            "manager_name": employee.manager_name,
            "skills_count": total_skills_rated,
            "average_rating": average_rating,
            "skills": skills_data
        })

    return employees_with_skills

async def employees_with_Skills(
        employees: List[employeeModel],
    skills_map: Dict[str, List[SkillBase]]
) -> List[Dict[str, Any]]:
    employees_with_skills = []
    for employee in employees:
        employee_skills = skills_map.get(employee.user_id, [])
        filtered_skills = [
            {k: v for k, v in skill.dict().items() if v is not None and v > 0} for skill in employee_skills
        ]
        employees_with_skills.append({
            "user_id": employee.user_id,
            "name": employee.name,
            "designation": employee.designation,
            "account": employee.account,
            "lead": employee.lead,
            "manager_name": employee.manager_name,
            "validated": employee.latest,
            "skills": filtered_skills
        })
    return employees_with_skills

async def fetch_employees_by_user_ids(
    db: AsyncSession,
    user_ids: List[str],
    employee:Optional[str]=None
) -> List[Any]:
    query = db.query(employeeModel).filter(employeeModel.user_id.in_(user_ids))
    return await run_in_executor(query.all)
