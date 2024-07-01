import asyncio
from typing import Any, Dict, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from models.Employee import MACH_Employee as employeeModel
from models.skills import Skills1
from models.user import User
import crud
from api import deps
from schemas.employee import EmployeeCreate
from sqlalchemy import and_, or_, func, case
from sqlalchemy.future import select
from typing import List
from schemas.employee import MACH_Employee,employeeSearchResults
from schemas.replacement_finder import ReplacementFinderResponse
from schemas.sme_finder import SmeFinder, SkillDetail
from schemas.talent_finder import TalentFinder
from schemas.Employee_with_skills import SkillBase
from services.service import *
from services.replacement_service import *
router = APIRouter()

@router.get("/{employee_id}", status_code=200, response_model=EmployeeCreate)
async def fetch_employee(
    *,
    employee_id: str,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    result = await crud.employee.get(db=db, id=employee_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"employee with ID {employee_id} not found")
    return result


@router.get("/", status_code=200)
async def root(
    request: Request,
    db: AsyncSession = Depends(deps.get_db),
):
    result = await crud.employee.get_multi(db=db)
    return { "employees": result}

@router.get("/onlyemployees/")
async def get_only_employees(
    db: Session = Depends(deps.get_db),
    name: Optional[List[str]] = Query(None, description="Filter by employee name"),
    designation: Optional[List[str]] = Query(None, description="Filter by employee designation"),
    account: Optional[List[str]] = Query(None, description="Filter by employee account"),
    lead: Optional[List[str]] = Query(None, description="Filter by employee lead"),
    manager_name: Optional[List[str]] = Query(None, description="Filter by employee manager name"),
    validated: Optional[List[str]] = Query(None, description="Filter by validated or not-validated"),
    tenure:Optional[List[str]] = Query(None, description="Filter by tenure"),
    iteration:Optional[List[int]] = Query(None, description="Filter by iteration"),
    capabilities:Optional[List[str]] = Query(None, description="Filter by capabilities"),
    serviceline_name:Optional[List[str]] = Query(None, description="Filter by seviceline"),
    function:Optional[List[str]] = Query(None, description="Filter by function"),
):
    employees = await fetch_employees(
        db, name, designation, account, lead, manager_name, validated,tenure,iteration,capabilities,serviceline_name,function)
    return employees


# @router.get("/talent_finder/",response_model=List[TalentFinder])
# async def talent_finder(
#     db: AsyncSession = Depends(deps.get_db),
#     name: Optional[str] = Query(None, description="Filter by employee name"),
#     designation: Optional[str] = Query(None, description="Filter by employee designation"),
#     account: Optional[str] = Query(None, description="Filter by employee account"),
#     lead: Optional[str] = Query(None, description="Filter by employee lead"),
#     manager_name: Optional[str] = Query(None, description="Filter by employee manager name"),
#     skill_name: Optional[str] = Query(None, description="Filter by skill name"),
#     rating: Optional[int] = Query(None, description="Filter by skill rating")
# ):
#     employees = await fetch_employees(db, name, designation, account, lead, manager_name)
#     if not employees:
#         raise HTTPException(status_code=404, detail="Employee(s) not found") 
#     filtered_skills = await fetch_skills(db, skill_name, rating)
#     skills_map = await map_skills(filtered_skills,skill_name,rating)
#     user_ids = list(skills_map.keys())
#     employee_user_ids = [employee.user_id for employee in employees]
#     user_ids = [user_id for user_id in skills_map.keys() if user_id in employee_user_ids]
#     employees_with_filtered_skills = await fetch_employees_by_user_ids(db, user_ids)
#     if not employees_with_filtered_skills:
#         raise HTTPException(status_code=404, detail="Employee(s) not found")
#     employees_with_skills = await process_employees_with_skills(employees_with_filtered_skills, skills_map)
#     return employees_with_skills

from sqlalchemy import select, join
@router.get("/talent_finder/")
async def talent_finder(
    db: AsyncSession = Depends(deps.get_db),
    name: Optional[List[str]] = Query(None, description="Filter by employee name"),
    designation: Optional[List[str]] = Query(None, description="Filter by employee designation"),
    account: Optional[List[str]] = Query(None, description="Filter by employee account"),
    lead: Optional[List[str]] = Query(None, description="Filter by employee lead"),
    manager_name: Optional[List[str]] = Query(None, description="Filter by employee manager name"),
    validated: Optional[List[str]] = Query(None, description="Filter by validated or not-validated"),
    tenure:Optional[List[str]] = Query(None, description="Filter by tenure"),
    iteration:Optional[List[int]] = Query(None, description="Filter by iteration"),
    capabilities:Optional[List[str]] = Query(None, description="Filter by capabilities"),
    serviceline_name:Optional[List[str]] = Query(None, description="Filter by seviceline"),
    functions:Optional[List[str]] = Query(None, description="Filter by function"),
    skill_name: Optional[List[str]] = Query(None, description="Filter by skill name"),
    rating: Optional[List[int]] = Query(None, description="Filter by skill rating"),
    # page: int = Query(1, description="Page number"),
    # page_size: int = Query(10, description="Number of items per page")
):
    rows =await fetch_employees(
        db, name, designation, account, lead, manager_name, validated,tenure,iteration,capabilities,serviceline_name,functions, skill_name, rating,
        
    )
    employees_with_skills = await process_employees_with_skills1(rows,rating,skill_name)
    return employees_with_skills
       
# @router.get("/sme_finder/")
# async def sme_finder(
#     db: AsyncSession = Depends(deps.get_db),
#     name: Optional[str] = Query(None, description="Filter by employee name"),
#     designation: Optional[str] = Query(None, description="Filter by employee designation"),
#     account: Optional[str] = Query(None, description="Filter by employee account"),
#     lead: Optional[str] = Query(None, description="Filter by employee lead"),
#     manager_name: Optional[str] = Query(None, description="Filter by employee manager name"),
#     validated: Optional[str] = Query(None, description="Filter by validated or not-validated"),
#     skill_name: Optional[str] = Query(None, description="Filter by skill name"),
#     rating: Optional[int] = Query(None, description="Filter by skill rating")
# ):
#     employees = await fetch_employees(db, name, designation, account, lead, manager_name, validated)
#     if not employees:
#         raise HTTPException(status_code=404, detail="Employee(s) not found")
#     filtered_skills = await fetch_skills(db, skill_name, rating)
#     skills_map = await map_skills(filtered_skills,skill_name,rating)
#     user_ids = list(skills_map.keys())
#     employee_user_ids = [employee.user_id for employee in employees]
#     user_ids = [user_id for user_id in skills_map.keys() if user_id in employee_user_ids]
#     employees_with_filtered_skills = await fetch_employees_by_user_ids(db, user_ids)
#     if not employees_with_filtered_skills:
#         raise HTTPException(status_code=404, detail="Employee(s) not found")
#     employees_with_skills = await employees_with_Skills(employees_with_filtered_skills, skills_map)
#     return employees_with_skills

# @router.get("/replacement_finder/")
# async def replacement_finder(
#     db: AsyncSession = Depends(deps.get_db),
#     name: Optional[str] = Query(None, description="Filter by employee name"),
#     designation: Optional[str] = Query(None, description="Filter by employee designation"),
#     account: Optional[str] = Query(None, description="Filter by employee account"),
#     validated: Optional[str] = Query(None, description="Filter by validated or not-validated"),
#     skill_name: Optional[str] = Query(None, description="Filter by skill name"),
#     rating: Optional[int] = Query(None, description="Filter by skill rating")
# ):
#     employees = await fetch_employees(db, name, designation, account, validated)
#     if not employees:
#         raise HTTPException(status_code=404, detail="Employee(s) not found")
#     filtered_skills = await fetch_skills(db, skill_name, rating)
#     skills_map = await map_skills_rf(filtered_skills)
#     user_ids = list(skills_map.keys())
#     employee_user_ids = [employee.user_id for employee in employees]
#     user_ids = [user_id for user_id in skills_map.keys() if user_id in employee_user_ids]
#     employees_average = await fetch_employees_average(db, user_ids)
#     if not employees_average:
#         raise HTTPException(status_code=404, detail="Employee(s) not found")
#     skill_avg_ratings = await calculate_skill_avg_ratings(db, user_ids, skill_name)
#     employees = await fetch_employees(db)
#     employees_with_skills = await process_employees_with_skills(employees, skills_map)
#     overall_avg_rating = await calculate_overall_avg_rating(skill_avg_ratings)
#     nearest_matches = await find_nearest_matches(employees_with_skills, overall_avg_rating)
#     return {"skill_avg_ratings": skill_avg_ratings,"overall_average_rating":overall_avg_rating,"nearest_matches": nearest_matches}

@router.get("/replacement_finder/")
async def replacement_finder(
    db: AsyncSession = Depends(deps.get_db),
    name: Optional[List[str]] = Query(None, description="Filter by employee name"),
    designation: Optional[List[str]] = Query(None, description="Filter by employee designation"),
    account: Optional[List[str]] = Query(None, description="Filter by employee account"),
    validated: Optional[List[str]] = Query(None, description="Filter by validated or not-validated"),
    skill_name: Optional[List[str]] = Query(None, description="Filter by skill name"),
    rating: Optional[List[int]] = Query(None, description="Filter by skill rating"),
    # page: int = Query(1, description="Page number"),
    # page_size: int = Query(10, description="Number of items per page")
    # current_user: User = Depends(deps.get_current_active_superuser),
):
    rows = await rf_fetch_employees(db, name,)    
    user_ids = [employee.user_id for employee in rows]
    # Calculate average skill ratings
    skill_avg_ratings = await calculate_skill_avg_ratings(db, user_ids,skill_name)
    if not skill_avg_ratings:
        raise HTTPException(status_code=404, detail="No skill ratings found")
    employees= await fetch_employees(db,designation=designation, account=account,validated=validated,skill_name=skill_name,rating=rating,)    
    employees_with_skills = await process_employees_with_skills1(employees,rating=rating,skill_query_name=skill_name)
    overall_avg_rating = await calculate_overall_avg_rating(skill_avg_ratings)
    nearest_matches = await find_nearest_matches(employees_with_skills, overall_avg_rating,skill_avg_rating=skill_avg_ratings)
    
    return {
        "skill_avg_ratings": skill_avg_ratings,
        "overall_average_rating": overall_avg_rating,
        "nearest_matches": nearest_matches
    }
from schemas.employee_skill_screen import EmployeeSkillScreen

@router.get("/employees_skill_screen/",response_model=EmployeeSkillScreen)
async def employees_skill_screen(
    db: AsyncSession = Depends(deps.get_db),
    serviceline: Optional[str] = Query(None, description="Filter by serviceline"),
    lead: Optional[str] = Query(None, description="Filter by lead"),
    manager: Optional[str] = Query(None, description="Filter by manager"),
    capabilities: Optional[str] = Query(None, description="Filter by capabilities"),
    designation: Optional[str] = Query(None, description="Filter by designation"),
    validation: Optional[str] = Query(None, description="Filter by validation"),
    iteration: Optional[str] = Query(None, description="Filter by iteration"),
    rating: Optional[int] = Query(None, description="Filter by rating")
):
    # Fetch employees
    query = select(employeeModel).join(Skills1, employeeModel.user_id == Skills1.user_id)
 
    if serviceline:
        query = query.where(employeeModel.serviceline_name == serviceline)
    if lead:
        query = query.where(employeeModel.lead == lead)
    if manager:
        query = query.where(employeeModel.manager_name == manager)
    if capabilities:
        query = query.where(employeeModel.capabilities == capabilities)
    if designation:
        query = query.where(employeeModel.designation == designation)
    if validation:
        query = query.where(employeeModel.validation == validation)
    if iteration:
        query = query.where(employeeModel.iteration == iteration)
 
    # Filter skills if rating is specified
    if rating is not None:
        for skill_column in Skills1.__table__.columns:
            if skill_column.name != 'EMP ID':
                query = query.where(getattr(Skills1, skill_column.name).isnot(None))
                query = query.where(getattr(Skills1, skill_column.name) == rating)
   
    result = db.execute(query)
    rows = result.scalars().all()
    user_ids = [employee.user_id for employee in rows]
 
    # Calculate average skill ratings
    skill_avg_ratings = await skill_avg_rating(db, user_ids)
   
    return {"skill_avg_ratings": skill_avg_ratings}

################################################################################################

# @router.get("/replacement_finder/")
# async def replacement_finder(
#     db: Session = Depends(deps.get_db),
#     name: Optional[str] = Query(None, description="Filter by employee name"),
#     designation: Optional[str] = Query(None, description="Filter by employee designation"),
#     account: Optional[str] = Query(None, description="Filter by employee account"),
#     validated: Optional[str] = Query(None, description="Filter by validated or not-validated"),
#     skill_name: Optional[str] = Query(None, description="Filter by skill name"),
#     rating: Optional[int] = Query(None, description="Filter by skill rating")
# ):
#     # Step 1: Filter Employees
#     employees_query = db.query(employeeModel)
#     if name:
#         employees_query = employees_query.filter(employeeModel.name.ilike(f"%{name}%"))
#     if designation:
#         employees_query = employees_query.filter(employeeModel.designation.ilike(f"%{designation}%"))
#     if account:
#         employees_query = employees_query.filter(employeeModel.account.ilike(f"%{account}%"))
#     if validated:
#         employees_query = employees_query.filter(employeeModel.latest == validated)
    
    

#     # Step 2: Filter Skills
#     skills_query = db.query(Skills1)
#     if skill_name:
#         skill_column = getattr(Skills1, skill_name.lower(), None)
#         if skill_column is not None:
#             if rating is not None:
#                 skills_query = skills_query.filter(skill_column == rating)
#             else:
#                 skills_query = skills_query.filter(skill_column.isnot(None))
    
#     skills = skills_query.all()

#     # Step 3: Calculate Average Ratings for each employee
#     skills_map = {}
#     for skill in skills:
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

#     user_ids = list(skills_map.keys())
#     employees_query = employees_query.filter(employeeModel.user_id.in_(user_ids))

#     employees = employees_query.all()
#     if not employees:
#         raise HTTPException(status_code=404, detail="Employee(s) not found")

#     employees_with_skills = []
#     for employee in employees:
#         employee_skills = skills_map.get(employee.user_id, [])
#         filtered_skills = [
#             {k: v for k, v in skill.dict().items() if v is not None} for skill in employee_skills
#         ]
#         total_skills_rated = sum(len(skill) for skill in filtered_skills)
#         average_rating = (sum(
#             value for skill in filtered_skills for value in skill.values()
#         ) / total_skills_rated) if total_skills_rated > 0 else 0
#         employees_with_skills.append({
#             "user_id": employee.user_id,
#             "name": employee.name,
#             "designation": employee.designation,
#             "account": employee.account,
#             "lead": employee.lead,
#             "manager_name": employee.manager_name,
#             "validated": employee.latest,
#             "skills": filtered_skills,
#             "total_skills_rated": total_skills_rated,
#             "average_rating": average_rating
#         })

#     # Step 4: Find the Nearest Match
#     selected_employee = employees_with_skills[0]  # Assuming the first employee is the selected one
#     selected_avg_rating = selected_employee['average_rating']

#     nearest_matches = []
#     for employee in employees_with_skills:
#         if employee['average_rating'] >= selected_avg_rating:
#             matching_skills = len(set(skill_name for skill in employee['skills'] for skill_name in skill.keys()))
#             employee['matching_skills'] = matching_skills
#             nearest_matches.append(employee)

#     # Step 5: Calculate average rating for each skill
#     skill_avg_ratings = {}
#     for skill_column in Skills1.__table__.columns:
#         if skill_column.name != 'user_id':
#             avg_rating = db.query(func.avg(skill_column)).scalar()
#             skill_avg_ratings[skill_column.name] = avg_rating

#     return {
#         "skill_avg_ratings": skill_avg_ratings,
#         "nearest_matches": nearest_matches
#     }

# @router.get("/employees/", response_model=List[EmployeeWithSkills])
# async def read_employees1(
#     db: Session = Depends(deps.get_db),
#     name: Optional[str] = Query(None, description="Filter by employee name"),
#     designation: Optional[str] = Query(None, description="Filter by employee designation"),
#     account: Optional[str] = Query(None, description="Filter by employee account"),
#     lead: Optional[str] = Query(None, description="Filter by employee lead"),
#     manager_name: Optional[str] = Query(None, description="Filter by employee manager name"),
#     python: Optional[int] = Query(None, description="Filter by Python skill rating"),
#     sql: Optional[int] = Query(None, description="Filter by SQL skill rating"),
#     excel: Optional[int] = Query(None, description="Filter by Excel skill rating"),
#     storyboarding: Optional[int] = Query(None, description="Filter by Storyboarding skill rating"),
#     business_communication : Optional[int] = Query(None, description ="Filter by business communication"),
#     result_orientation: Optional[int] = Query(None, description="Filter by result orientation"),
#     quality_focus: Optional[int] = Query(None, description="Filter by quality focus"),
#     effective_communication: Optional[int] = Query(None, description="Filter by effective communication"),
#     work_management_and_effectiveness: Optional[int] = Query(None, description="Filter by work management and effectiveness"),
#     client_centric: Optional[int] = Query(None, description="Filter by client centric"),
#     genai: Optional[int] = Query(None, description="Filter by GenAI"),
#     nuclios: Optional[int] = Query(None, description="Filter by NucliOS")
# ):
#     # Base query for employees
#     employees_query = db.query(employeeModel)

#     # Apply filters for employees
      
#     # Fetch the user_ids of filtered employees
#     # user_ids = [employee.user_id for employee in employees]

#     # Base query for skills
#     skills_query = db.query(Skills1)

#     if python is not None:
#         skills_query = skills_query.filter(Skills1.python == python)
#     if sql is not None:
#         skills_query = skills_query.filter(Skills1.sql == sql)
#     if excel is not None:
#         skills_query = skills_query.filter(Skills1.excel == excel)
#     if storyboarding is not None:
#         skills_query = skills_query.filter(Skills1.storyboarding == storyboarding)
#     if business_communication is not None:
#         skills_query = skills_query.filter(Skills1.business_communication == business_communication)
#     if result_orientation is not None:
#         skills_query = skills_query.filter(Skills1.result_orientation == result_orientation)
#     if quality_focus is not None:
#         skills_query = skills_query.filter(Skills1.quality_focus == quality_focus)
#     if effective_communication is not None:
#         skills_query = skills_query.filter(Skills1.effective_communication == effective_communication)
#     if work_management_and_effectiveness is not None:
#         skills_query = skills_query.filter(Skills1.work_management_and_effectiveness == work_management_and_effectiveness)
#     if client_centric is not None:
#         skills_query = skills_query.filter(Skills1.clientcentric == client_centric)
#     if genai is not None:
#         skills_query = skills_query.filter(Skills1.genai == genai)
#     if nuclios is not None:
#         skills_query = skills_query.filter(Skills1.nuclios == nuclios)
    
#     # Fetch the skills
#     skills = skills_query.all()
#     # print(skills)

#     # Create a map from user_id to skills
#     skills_map = {}
#     for skill in skills:
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

#     user_ids = list(skills_map.keys())

#     # Base query for employees
#     employees_query = db.query(employeeModel).filter(employeeModel.user_id.in_(user_ids))

#     if name is not None:
#         employees_query = employees_query.filter(employeeModel.name == name)
#     if designation is not None:
#         employees_query = employees_query.filter(employeeModel.designation == designation)
#     if account is not None:
#         employees_query = employees_query.filter(employeeModel.account == account)
#     if lead is not None:
#         employees_query = employees_query.filter(employeeModel.lead == lead)
#     if manager_name is not None:
#         employees_query = employees_query.filter(employeeModel.manager_name == manager_name)
    
#     employees = employees_query.all()

#     if not employees:
#         raise HTTPException(status_code=404, detail="Employee(s) not found")  

#     # Convert to Pydantic model
#     employees_with_skills = [
#         EmployeeWithSkills(
#             user_id=employee.user_id,
#             name=employee.name,
#             designation=employee.designation,
#             account=employee.account,
#             lead=employee.lead,
#             manager_name=employee.manager_name,
#             skills=skills_map[employee.user_id]
#         ) for employee in employees
#     ]
#     return employees_with_skills


@router.get("/search/", status_code=200, response_model=employeeSearchResults)
async def search_employees(
    *,
    keyword: str = Query(None, min_length=3, example="MACH"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for employees based on label keyword
    """
    employees =await crud.employee.get_multi(db=db, limit=max_results)
    results = filter(lambda employee: keyword.lower() in employee.name.lower(), employees)

    return {"results": list(results)[:5]}

