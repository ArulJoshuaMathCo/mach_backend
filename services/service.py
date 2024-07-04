from typing import Optional, List, Dict, Any, Union
from sqlalchemy.orm import Session, selectinload, aliased
from sqlalchemy.future import select
from sqlalchemy import func, or_, case, and_, literal, distinct
from concurrent.futures import ThreadPoolExecutor
import asyncio
from decimal import Decimal
from models.Employee import MACH_Employee as employeeModel
from models.skills import Skills1
from schemas.Employee_with_skills import SkillBase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Query

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
    tenure: Optional[List[str]]= None,
    iteration: Optional[List[int]]= None,
    capabilities: Optional[List[str]]= None,
    serviceline_name: Optional[List[str]]= None,
    function: Optional[List[str]]= None,
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
        query = query.where(employeeModel.validation.in_(validated))
    if tenure:
        query = query.where(employeeModel.tenure.in_(tenure))
    if iteration:
        query = query.where(employeeModel.iteration.in_(iteration))
    if capabilities:
        query = query.where(employeeModel.capabilities.in_(capabilities))
    if serviceline_name:
        query = query.where(employeeModel.serviceline_name.in_(serviceline_name))
    if function:
        query = query.where(employeeModel.function.in_(function))
    if skill_name is not None and rating is not None:
        # Create AND conditions for both skill name and rating
        skill_rating_conditions = [
            or_(getattr(Skills1, skill.lower(), None) == rate) 
            for skill in skill_name 
            for rate in rating 
            if getattr(Skills1, skill.lower(), None) is not None
        ]
        if skill_rating_conditions:
            query = query.where(or_(*skill_rating_conditions))
    elif skill_name is not None:
        # Create OR conditions for skill names
        skill_conditions = [getattr(Skills1, skill.lower(), None).isnot(None) for skill in skill_name if getattr(Skills1, skill.lower(), None) is not None]
        if skill_conditions:
            query = query.where(or_(*skill_conditions))
    elif rating is not None:
        # Construct OR condition for all columns of Skills1
        or_conditions = [
            column == rate 
            for column in Skills1.__table__.columns 
            if column.name != 'user_id'  # Exclude user_id column from filtering
            for rate in rating
        ]
        query = query.where(or_(*or_conditions))
    
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
            "validated": employee.validation,
            "skills": filtered_skills,
            "total_skills_rated": total_skills_rated,
            "average_rating": average_rating
        })
    return employees_with_skills

async def skill_avg_rating(
    db: AsyncSession,
    user_ids: List[str],
    skill_name: Optional[str]
) -> List[Dict[str, Optional[float]]]:
    skill_avg_ratings = []
    for skill_column in Skills1.__table__.columns:
        if skill_column.name != 'user_id':
            avg_rating_query = select(
                func.avg(skill_column).label('average_rating'),
                func.count(skill_column).label('employee_count')
            ).filter(
                skill_column.isnot(None),
                Skills1.user_id.in_(user_ids)
            )
            if skill_name:
                avg_rating_query = avg_rating_query.filter(getattr(Skills1, skill_name.lower(), None).isnot(None))
           
            result = db.execute(avg_rating_query)
            avg_rating, employee_count = result.one_or_none()
 
            if avg_rating is not None:
                skill_avg_ratings.append({
                    "skill_name": skill_column.name,
                    "average_rating": avg_rating,
                    "employee_count": employee_count
                })
            else:
                skill_avg_ratings.append({
                    "skill_name": skill_column.name,
                    "average_rating": None,
                    "employee_count": 0
                })
    return skill_avg_ratings
from sqlalchemy.orm.properties import ColumnProperty
def create_dynamic_mapping(model) -> Dict[str, str]:
    attribute_to_column = {}
    for prop in model.__mapper__.iterate_properties:
        if isinstance(prop, ColumnProperty):
            for column in prop.columns:
                attribute_to_column[prop.key] = column.name
    return attribute_to_column

async def process_employees_with_skills1(
    employees: List[employeeModel],
    rating: Optional[List[int]] = None,
    skill_query_name: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    employees_with_skills = []

    # Create a dynamic mapping of attribute names to actual column names
    attribute_to_column = create_dynamic_mapping(Skills1)

    for employee in employees:
        total_skills_rated = 0
        total_rating = 0
        skills_data = {}

        # Ensure employee.skills is loaded and not empty
        if employee.skills:
            # Iterate over the attributes of the skills object
            for skill in employee.skills:
                for skill_attr, skill_value in skill.__dict__.items():
                    if skill_attr != 'user_id' and skill_attr != '_sa_instance_state' and isinstance(skill_value, (int, float)):  # Exclude user_id column

                        total_skills_rated += 1
                        total_rating += skill_value

                        # Get the actual column name
                        skill_column_name = attribute_to_column.get(skill_attr, None)
                        if skill_column_name is None:
                            print(f"Attribute {skill_attr} not found in model columns mapping.")
                            continue

                        if rating and skill_query_name is not None:
                            for query_skill in skill_query_name:
                                for rate in rating:
                                    if rate == skill_value and query_skill == skill_column_name:
                                        skills_data[skill_column_name] = skill_value
                        elif rating is not None and skill_query_name is None:
                            for rate in rating:
                                if rate is None or rate == skill_value:
                                    skills_data[skill_column_name] = skill_value
                        elif skill_query_name is not None and rating is None:
                            for query_skill in skill_query_name:
                                if query_skill is None or query_skill == skill_column_name:
                                    skills_data[skill_column_name] = skill_value
                        else:
                            if rating is None and skill_query_name is None:
                                skills_data[skill_column_name] = skill_value

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
            "tenure": employee.tenure,
            "iteration": employee.iteration,
            "capabilities": employee.capabilities,
            "serviceline_name": employee.serviceline_name,
            "validation": employee.validation,
            "functions": employee.function,
            "skills_count": total_skills_rated,
            "average_rating": average_rating,
            "skills": skills_data
        })

    return employees_with_skills
# async def process_employees_with_skills1(
#     employees: List[employeeModel],
#     rating:Optional[List[int]]=None,
#     skill_query_name:Optional[List[str]]= None
# ) -> List[Dict[str, Any]]:
#     employees_with_skills = []
    # for employee in employees:
    #     total_skills_rated = 0
    #     total_rating = 0
    #     skills_data = {}

    #     # Ensure employee.skills is loaded and not empty
    #     if employee.skills:
    #         # Iterate over the attributes of the skills object
    #         for skill in employee.skills:
    #             for skill_name, skill_value in skill.__dict__.items():
    #                 if skill_name != 'user_id' and skill_name != '_sa_instance_state' and isinstance(skill_value, (int, float)):  # Exclude user_id column
                        
    #                     total_skills_rated += 1
    #                     total_rating += skill_value
    #                     if rating and skill_query_name is not None:
    #                         for skill in skill_query_name:
    #                             for rate in rating:
    #                                 if rate==skill_value and skill == skill_name:
    #                                     skills_data[skill_name] = skill_value
    #                     elif rating is not None and skill_query_name is None:
    #                         for rate in rating:
    #                             if rate is None or rate==skill_value:
    #                                 skills_data[skill_name] = skill_value
    #                     elif skill_query_name is not None and rating is None:
    #                         for skill in skill_query_name:
    #                             if skill is None or skill == skill_name:
    #                                 skills_data[skill_name] = skill_value
    #                     else:
                            
    #                         if rating is None and skill_query_name is not None:
    #                             skills_data[skill_name] = skill_value

    #         average_rating = (total_rating / total_skills_rated) if total_skills_rated > 0 else 0
    #     else:
    #         average_rating = 0

    #     employees_with_skills.append({
    #         "user_id": employee.user_id,
    #         "name": employee.name,
    #         "designation": employee.designation,
    #         "account": employee.account,
    #         "lead": employee.lead,
    #         "manager_name": employee.manager_name,
    #         "tenure":employee.tenure,
    #         "iteration":employee.iteration,
    #         "capabilities":employee.capabilities,
    #         "serviceline_name":employee.serviceline_name,
    #         "function":employee.function,
    #         "skills_count": total_skills_rated,
    #         "average_rating": average_rating,
    #         "skills": skills_data
    #     })

    # return employees_with_skills
    # attribute_to_column = {
    #     "user_id": "EMP ID",
    #     "python": "Python",
    #     "sql": "SQL",
    #     "excel": "Excel",
    #     "storyboarding": "Storyboarding",
    #     "business_communication": "Business Communication",
    #     "javascript": "Javascript",
    #     "exploratory_data_analysis": "Exploratory Data Analysis",
    #     # Add more mappings as necessary
    # }

    # for employee in employees:
    #     total_skills_rated = 0
    #     total_rating = 0
    #     skills_data = {}

    #     # Ensure employee.skills is loaded and not empty
    #     if employee.skills:
    #         # Iterate over the attributes of the skills object
    #         for skill in employee.skills:
    #             for skill_attr, skill_value in skill.__dict__.items():
    #                 if skill_attr != 'user_id' and skill_attr != '_sa_instance_state' and isinstance(skill_value, (int, float)):  # Exclude user_id column

    #                     total_skills_rated += 1
    #                     total_rating += skill_value

    #                     # Get the actual column name
    #                     skill_column_name = attribute_to_column.get(skill_attr, None)
    #                     if skill_column_name is None:
    #                         print(f"Attribute {skill_attr} not found in model columns mapping.")
    #                         continue

    #                     if rating and skill_query_name is not None:
    #                         for query_skill in skill_query_name:
    #                             for rate in rating:
    #                                 if rate == skill_value and query_skill == skill_column_name:
    #                                     skills_data[skill_column_name] = skill_value
    #                     elif rating is not None and skill_query_name is None:
    #                         for rate in rating:
    #                             if rate is None or rate == skill_value:
    #                                 skills_data[skill_column_name] = skill_value
    #                     elif skill_query_name is not None and rating is None:
    #                         for query_skill in skill_query_name:
    #                             if query_skill is None or query_skill == skill_column_name:
    #                                 skills_data[skill_column_name] = skill_value
    #                     else:
    #                         if rating is None and skill_query_name is None:
    #                             skills_data[skill_column_name] = skill_value

    #         average_rating = (total_rating / total_skills_rated) if total_skills_rated > 0 else 0
    #     else:
    #         average_rating = 0

    #     employees_with_skills.append({
    #         "user_id": employee.user_id,
    #         "name": employee.name,
    #         "designation": employee.designation,
    #         "account": employee.account,
    #         "lead": employee.lead,
    #         "manager_name": employee.manager_name,
    #         "tenure": employee.tenure,
    #         "iteration": employee.iteration,
    #         "capabilities": employee.capabilities,
    #         "serviceline_name": employee.serviceline_name,
    #         "function": employee.function,
    #         "skills_count": total_skills_rated,
    #         "average_rating": average_rating,
    #         "skills": skills_data
    #     })

    # return employees_with_skills

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

# async def calculate_skill_avg_ratings(db: Session, user_ids: List[str], skill_name: Optional[str]):
#     # Dynamically calculate average ratings for each skill
#     if skill_name:
#         skill_column = getattr(Skills1, skill_name.lower(), None)
#         if not skill_column:
#             return []
#         avg_rating = func.avg(skill_column).label("average_rating")
#         count_people = func.sum(case([(skill_column != None, 1)], else_=0)).label("number_of_people")
#         query = select(
#             avg_rating,
#             count_people
#         ).where(Skills1.user_id.in_(user_ids)).filter(skill_column.isnot(None))
        
#         result = db.execute(query).first()
#         if result:
#             avg, count = result
#             return [{
#                 "skill_name": skill_name,
#                 "average_rating": avg,
#                 "number_of_people": count
#             }]
#     else:
#         skill_columns = Skills1.__table__.columns.keys()
#         results = []
#         for skill in skill_columns:
#             if skill in ["user_id"]:
#                 continue
#             skill_column = getattr(Skills1, skill, None)
#             avg_rating = func.avg(skill_column).label("average_rating")
#             count_people = func.sum(case([(skill_column != None, 1)], else_=0)).label("number_of_people")
#             query = select(
#                 avg_rating,
#                 count_people
#             ).where(Skills1.user_id.in_(user_ids)).filter(skill_column.isnot(None))
            
#             result = db.execute(query).first()
#             if result:
#                 avg, count = result
#                 if avg is not None and count > 0:
#                     results.append({
#                         "skill_name": skill,
#                         "average_rating": avg,
#                         "number_of_people": count
#                     })
#         return results

# async def skill_avg_rating(
#     db: AsyncSession,
#     user_ids: List[str],
#     rating: Optional[int]
# ) -> List[Dict[str, Optional[float]]]:
#     skill_avg_ratings = []
#     for skill_column in Skills1.__table__.columns:
#         if skill_column.name != 'EMP ID':
#             avg_rating_query = select(
#                 func.avg(skill_column).label('average_rating'),
#                 func.count().label('employee_count')
#             ).filter(
#                 skill_column.isnot(None),
#                 Skills1.user_id.in_(user_ids),
#                 skill_column.in_([1, 2, 3, 4, 5])
#             )
#             if rating is not None:
#                 avg_rating_query = avg_rating_query.filter(skill_column == rating)
            
#             result = db.execute(avg_rating_query)
#             avg_rating, employee_count = result.one_or_none()

#             if avg_rating is not None:
#                 skill_avg_ratings.append({
#                     "skill_name": skill_column.name,
#                     "average_rating": avg_rating,
#                     "employee_count": employee_count
#                 })
#             else:
#                 skill_avg_ratings.append({
#                     "skill_name": skill_column.name,
#                     "average_rating": None,
#                     "employee_count": 0
#                 })
#     return skill_avg_ratings

# async def fetch_service_line_percentages(
#     db: AsyncSession,
#     user_ids: List[str],
#     skill_name: Optional[str] = None
# ):
#     # Fetch total employee count
#     total_count = db.execute(select(func.count(employeeModel.user_id)))
#     total_employees = total_count.scalar()

#     # Fetch employee count per service line
#     query = select(
#         employeeModel.serviceline_name,
#         func.count(employeeModel.user_id)
#     ).group_by(employeeModel.serviceline_name)

#     if user_ids:
#         query = query.where(employeeModel.user_id.in_(user_ids))

#     serviceline_counts = db.execute(query)
#     serviceline_counts = serviceline_counts.all()

#     # Calculate percentage of employees per service line
#     serviceline_percentages = [
#         {
#             "serviceline_name": line[0],
#             "employee_percentage": (line[1] / total_employees) * 100,
#             "skill_percentages": await get_skill_percentages_by_serviceline(db, line[0], user_ids, skill_name=skill_name)  # Fetch skill percentages for each service line
#         }
#         for line in serviceline_counts
#     ]

#     return serviceline_percentages

# async def get_skill_percentages_by_serviceline(db: AsyncSession, serviceline_name: str, user_ids: List[str], skill_name: Optional[str] = None) -> List[Dict[str, Any]]:
#     skill_percentages = []
    
#     # Fetch total employees in the specified service line
#     query = select(func.count()).where(employeeModel.serviceline_name == serviceline_name)
#     total_serviceline_employees = db.execute(query).scalar()
    
#     for skill_column in Skills1.__table__.columns:
#         if skill_column.name != 'EMP ID' and (skill_name is None or skill_column.name == skill_name):
#             result = db.execute(
#                 select(func.count(skill_column))
#                 .join(employeeModel, employeeModel.user_id == Skills1.user_id)
#                 .where(
#                     employeeModel.serviceline_name == serviceline_name,
#                     skill_column.isnot(None),
#                     skill_column.in_([1, 2, 3, 4, 5])
#                 )
#             )
            
#             skill_count = result.scalar()
#             skill_percentages.append({
#                 "skill": skill_column.name,
#                 "percentage": (skill_count / total_serviceline_employees) * 100,
#                 "rating_percentages": await get_skill_rating_percentages(db, serviceline_name, skill_column.name, user_ids)
#             })
#     return skill_percentages

# async def get_skill_rating_percentages(db: AsyncSession, serviceline_name: str, skill_column_name: str, user_ids: List[str]) -> List[Dict[str, Any]]:
#     skill_rating_percentages = []

#     # Fetch total employees in the specified service line
#     query = select(func.count()).where(employeeModel.serviceline_name == serviceline_name)
#     total_serviceline_employees = db.execute(query).scalar()
    
#     # Fetch rating counts for the given skill and service line
#     result = db.execute(
#         select(Skills1.__table__.columns[skill_column_name], func.count(Skills1.__table__.columns[skill_column_name]))
#         .join(employeeModel, employeeModel.user_id == Skills1.user_id)
#         .where(
#             Skills1.__table__.columns[skill_column_name].in_([1, 2, 3, 4, 5]),  # Filter for ratings 1 to 5
#             employeeModel.serviceline_name == serviceline_name,
#             employeeModel.user_id.in_(user_ids)
#         )
#         .group_by(Skills1.__table__.columns[skill_column_name])
#     )
#     rating_counts = result.all()
    
#     for rating, count in rating_counts:
#         skill_rating_percentages.append({
#             "rating": rating,
#             "percentage": (count / total_serviceline_employees) * 100
#         })
    
#     return skill_rating_percentages

async def fetch_service_line_percentages(
    db: AsyncSession,
    user_ids: List[str],
    skill_name: Optional[str] = None
):
    # Fetch total employee count
    total_count = db.execute(select(func.count(employeeModel.user_id)))
    total_employees = total_count.scalar()

    # Fetch employee count per service line
    query = select(
        employeeModel.serviceline_name,
        func.count(employeeModel.user_id)
    ).group_by(employeeModel.serviceline_name)

    if user_ids:
        query = query.where(employeeModel.user_id.in_(user_ids))

    serviceline_counts = db.execute(query)
    serviceline_counts = serviceline_counts.all()

    # Calculate percentage of employees per service line
    serviceline_percentages = [
        {
            "serviceline_name": line[0],
            "number_of_employees": line[1],
            "employee_percentage": (line[1] / total_employees) * 100,
            "average_rating": await get_average_rating_for_serviceline(db, line[0], user_ids),
            "skill_percentages": await get_skill_percentages_by_serviceline(db, line[0], user_ids, skill_name=skill_name)  # Fetch skill percentages for each service line
        }
        for line in serviceline_counts
    ]

    return serviceline_percentages

async def get_skill_percentages_by_serviceline(db: AsyncSession, serviceline_name: str, user_ids: List[str], skill_name: Optional[str] = None) -> List[Dict[str, Any]]:
    skill_percentages = []
    
    # Fetch total employees in the specified service line
    query = select(func.count()).where(employeeModel.serviceline_name == serviceline_name)
    total_serviceline_employees = (db.execute(query)).scalar()
    
    for skill_column in Skills1.__table__.columns:
        if skill_column.name != 'EMP ID' and (skill_name is None or skill_column.name == skill_name):
            result = db.execute(
                select(func.count(skill_column))
                .join(employeeModel, employeeModel.user_id == Skills1.user_id)
                .where(
                    employeeModel.serviceline_name == serviceline_name,
                    skill_column.isnot(None),
                    skill_column.in_([1, 2, 3, 4, 5])
                )
            )
            
            skill_count = result.scalar()
            total_skill_ratings = db.execute(
                select(func.sum(skill_column))
                .join(employeeModel, employeeModel.user_id == Skills1.user_id)
                .where(
                    employeeModel.serviceline_name == serviceline_name,
                    skill_column.isnot(None),
                    skill_column.in_([1, 2, 3, 4, 5])
                )
            )
            total_skill_ratings = total_skill_ratings.scalar()
            average_rating = (total_skill_ratings / skill_count) if skill_count else 0
            
            skill_percentages.append({
                "skill": skill_column.name,
                "number_of_employees": skill_count,
                "percentage": (skill_count / total_serviceline_employees) * 100,
                "average_rating": average_rating,
                "rating_percentages": await get_skill_rating_percentages(db, serviceline_name, skill_column.name, user_ids)
            })
    return skill_percentages

async def get_skill_rating_percentages(db: AsyncSession, serviceline_name: str, skill_column_name: str, user_ids: List[str]) -> List[Dict[str, Any]]:
    skill_rating_percentages = []

    # Fetch total employees in the specified service line
    query = select(func.count()).where(employeeModel.serviceline_name == serviceline_name)
    total_serviceline_employees = (db.execute(query)).scalar()
    
    # Fetch rating counts for the given skill and service line
    result = db.execute(
        select(Skills1.__table__.columns[skill_column_name], func.count(Skills1.__table__.columns[skill_column_name]))
        .join(employeeModel, employeeModel.user_id == Skills1.user_id)
        .where(
            Skills1.__table__.columns[skill_column_name].in_([1, 2, 3, 4, 5]),  # Filter for ratings 1 to 5
            employeeModel.serviceline_name == serviceline_name,
            employeeModel.user_id.in_(user_ids)
        )
        .group_by(Skills1.__table__.columns[skill_column_name])
    )
    rating_counts = result.all()
    
    for rating, count in rating_counts:
        skill_rating_percentages.append({
            "rating": rating,
            "number_of_employees": count,
            "percentage": (count / total_serviceline_employees) * 100
        })
    
    return skill_rating_percentages

async def get_average_rating_for_serviceline(db: AsyncSession, serviceline_name: str, user_ids: List[str]) -> float:
    total_ratings = 0
    total_count = 0
    
    for skill_column in Skills1.__table__.columns:
        if skill_column.name != 'EMP ID':
            result = db.execute(
                select(func.sum(skill_column), func.count(skill_column))
                .join(employeeModel, employeeModel.user_id == Skills1.user_id)
                .where(
                    employeeModel.serviceline_name == serviceline_name,
                    skill_column.isnot(None),
                    skill_column.in_([1, 2, 3, 4, 5])
                )
            )
            sum_ratings, count_ratings = result.one()
            total_ratings += sum_ratings or 0
            total_count += count_ratings or 0

    return (total_ratings / total_count) if total_count else 0

# SPECIFIC_SKILLS = ['python', 'sql', 'statistics', 'business_communication', 'excel']

# async def fetch_service_line_percentages(
#     db: AsyncSession,
#     user_ids: List[str],
#     skill_name: Optional[str] = None
# ):
#     # Fetch total employee count
#     total_count = db.execute(select(func.count(employeeModel.user_id)))
#     total_employees = total_count.scalar()

#     # Fetch employee count per service line
#     query = select(
#         employeeModel.serviceline_name,
#         func.count(employeeModel.user_id)
#     ).group_by(employeeModel.serviceline_name)

#     if user_ids:
#         query = query.where(employeeModel.user_id.in_(user_ids))

#     serviceline_counts = db.execute(query)
#     serviceline_counts = serviceline_counts.all()

#     # Calculate percentage of employees per service line
#     serviceline_percentages = [
#         {
#             "serviceline_name": line[0],
#             "employee_percentage": (line[1] / total_employees) * 100,
#             "average_rating": await get_average_rating_for_serviceline(db, line[0], user_ids),
#             "skill_percentages": await get_skill_percentages_by_serviceline(db, line[0], user_ids, skill_name=skill_name)  # Fetch skill percentages for each service line
#         }
#         for line in serviceline_counts
#     ]

#     return serviceline_percentages

# async def get_skill_percentages_by_serviceline(db: AsyncSession, serviceline_name: str, user_ids: List[str], skill_name: Optional[str] = None) -> List[Dict[str, Any]]:
#     skill_percentages = []
    
#     # Fetch total employees in the specified service line
#     query = select(func.count()).where(employeeModel.serviceline_name == serviceline_name)
#     total_serviceline_employees = (db.execute(query)).scalar()
    
#     for skill_column in Skills1.__table__.columns:
#         if skill_column.name in SPECIFIC_SKILLS and (skill_name is None or skill_column.name == skill_name):
#             result = await db.execute(
#                 select(func.count(skill_column))
#                 .join(employeeModel, employeeModel.user_id == Skills1.user_id)
#                 .where(
#                     employeeModel.serviceline_name == serviceline_name,
#                     skill_column.isnot(None),
#                     skill_column.in_([1, 2, 3, 4, 5])
#                 )
#             )
            
#             skill_count = result.scalar()
#             total_skill_ratings = await db.execute(
#                 select(func.sum(skill_column))
#                 .join(employeeModel, employeeModel.user_id == Skills1.user_id)
#                 .where(
#                     employeeModel.serviceline_name == serviceline_name,
#                     skill_column.isnot(None),
#                     skill_column.in_([1, 2, 3, 4, 5])
#                 )
#             )
#             total_skill_ratings = total_skill_ratings.scalar()
#             average_rating = (total_skill_ratings / skill_count) if skill_count else 0
            
#             skill_percentages.append({
#                 "skill": skill_column.name,
#                 "percentage": (skill_count / total_serviceline_employees) * 100,
#                 "average_rating": average_rating,
#                 "rating_percentages": await get_skill_rating_percentages(db, serviceline_name, skill_column.name, user_ids)
#             })
#     return skill_percentages

# async def get_skill_rating_percentages(db: AsyncSession, serviceline_name: str, skill_column_name: str, user_ids: List[str]) -> List[Dict[str, Any]]:
#     skill_rating_percentages = []

#     # Fetch total employees in the specified service line
#     query = select(func.count()).where(employeeModel.serviceline_name == serviceline_name)
#     total_serviceline_employees = (await db.execute(query)).scalar()
    
#     # Fetch rating counts for the given skill and service line
#     result = await db.execute(
#         select(Skills1.__table__.columns[skill_column_name], func.count(Skills1.__table__.columns[skill_column_name]))
#         .join(employeeModel, employeeModel.user_id == Skills1.user_id)
#         .where(
#             Skills1.__table__.columns[skill_column_name].in_([1, 2, 3, 4, 5]),  # Filter for ratings 1 to 5
#             employeeModel.serviceline_name == serviceline_name,
#             employeeModel.user_id.in_(user_ids)
#         )
#         .group_by(Skills1.__table__.columns[skill_column_name])
#     )
#     rating_counts = result.all()
    
#     for rating, count in rating_counts:
#         skill_rating_percentages.append({
#             "rating": rating,
#             "percentage": (count / total_serviceline_employees) * 100
#         })
    
#     return skill_rating_percentages

# async def get_average_rating_for_serviceline(db: AsyncSession, serviceline_name: str, user_ids: List[str]) -> float:
#     total_ratings = 0
#     total_count = 0
    
#     for skill_column in Skills1.__table__.columns:
#         if skill_column.name in SPECIFIC_SKILLS:
#             result = await db.execute(
#                 select(func.sum(skill_column), func.count(skill_column))
#                 .join(employeeModel, employeeModel.user_id == Skills1.user_id)
#                 .where(
#                     employeeModel.serviceline_name == serviceline_name,
#                     skill_column.isnot(None),
#                     skill_column.in_([1, 2, 3, 4, 5])
#                 )
#             )
#             sum_ratings, count_ratings = result.one()
#             total_ratings += sum_ratings or 0
#             total_count += count_ratings or 0

#     return (total_ratings / total_count) if total_count else 0
