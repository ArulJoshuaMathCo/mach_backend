import asyncio
from typing import Any, Dict, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from models.Employee import MACH_Employee as employeeModel
from models.skills import Skills1
import crud
import deps
from schemas.employee import EmployeeCreate
from sqlalchemy import and_, or_
from typing import List
from schemas.employee import MACH_Employee
from schemas.Employee_with_skills import EmployeeWithSkills,SkillBase
router = APIRouter()
employee_SUBREDDITS = ["employees", "easyemployees", "TopSecretemployees"]


@router.get("/{employee_id}", status_code=200, response_model=EmployeeCreate)
async def fetch_employee(
    *,
    employee_id: str,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single employee by ID
    """
    result = await crud.employee.get(db=db, id=employee_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"employee with ID {employee_id} not found"
        )

    return result


@router.get("/", status_code=200)
async def root(
    request: Request,
    db: Session = Depends(deps.get_db),
):
    """
    Root GET
    """
    result = await crud.employee.get_multi(db=db)
    return { "employees": result}

@router.get("/onlyemployees/", response_model=List[MACH_Employee])
async def get_only_employees(
    db: Session = Depends(deps.get_db),
    name: str = Query(None, description="Filter by employee name"),
    designation: str = Query(None, description="Filter by employee designation"),
    account: str = Query(None, description="Filter by employee account"),
    lead: str = Query(None, description="Filter by employee lead"),
    manager_name: str = Query(None, description="Filter by employee manager name"),
):
    filters = []
    if name:
        filters.append(employeeModel.name == name)
    if designation:
        filters.append(employeeModel.designation == designation)
    if account:
        filters.append(employeeModel.account == account)
    if lead:
        filters.append(employeeModel.lead == lead)
    if manager_name:
        filters.append(employeeModel.manager_name == manager_name)

    query = db.query(employeeModel)
    if filters:
        query = query.filter(and_(*filters))

    employees = query.all()
    return employees


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

@router.get("/talent_finder/")
async def talent_finder(
    db: Session = Depends(deps.get_db),
    name: Optional[str] = Query(None, description="Filter by employee name"),
    designation: Optional[str] = Query(None, description="Filter by employee designation"),
    account: Optional[str] = Query(None, description="Filter by employee account"),
    lead: Optional[str] = Query(None, description="Filter by employee lead"),
    manager_name: Optional[str] = Query(None, description="Filter by employee manager name"),
    skills: Optional[str] = Query(None, description="Filter by skill name"),
    rating: Optional[int] = Query(None, description="Filter by skill rating")
):
    # Base query for employees
    employees_query = db.query(employeeModel)

    # Apply filters for employees
    if name is not None:
        employees_query = employees_query.filter(employeeModel.name == name)
    if designation is not None:
        employees_query = employees_query.filter(employeeModel.designation == designation)
    if account is not None:
        employees_query = employees_query.filter(employeeModel.account == account)
    if lead is not None:
        employees_query = employees_query.filter(employeeModel.lead == lead)
    if manager_name is not None:
        employees_query = employees_query.filter(employeeModel.manager_name == manager_name)
    
    # Base query for skills
    skills_query = db.query(Skills1)

    if skills is not None and rating is not None:
        # Assuming skills are filtered based on the lowercase version of their names
        skill_column = getattr(Skills1, skills.lower(), None)
        if skill_column is not None:
            skills_query = skills_query.filter(skill_column == rating)
    if skills is not None and rating is None:
        skill_column = getattr(Skills1,skills.lower(),None)
        if skill_column is not None:
            skills_query = skills_query.filter(skill_column.isnot(None))
    if skills is None and rating is not None:
        # Construct OR condition for all columns of Skills1
        or_conditions = []
        for column in Skills1.__table__.columns:
            if column.name != 'user_id':  # Exclude user_id column from filtering
                or_conditions.append(column == rating)
        
        # Apply the OR conditions to the query
        skills_query = skills_query.filter(or_(*or_conditions))
    # Fetch the skills
    skills = skills_query.all()

    # Create a map from user_id to skills
    skills_map = {}
    for skill in skills:
        if skill.user_id not in skills_map:
            skills_map[skill.user_id] = SkillBase(
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
            )

    user_ids = list(skills_map.keys())

    # Query employees with the filtered user_ids
    employees_query = employees_query.filter(employeeModel.user_id.in_(user_ids))
    employees = employees_query.all()

    if not employees:
        raise HTTPException(status_code=404, detail="Employee(s) not found")

    # Create employees with skills and calculate total_skills_rated and average_rating
    employees_with_skills = []
    for employee in employees:
        employee_skills = skills_map.get(employee.user_id)
        if employee_skills:
            # Calculate total_skills_rated
            total_skills_rated = sum(1 for skill_value in dict(employee_skills).values() if skill_value is not None)
            # Calculate average_rating
            rated_skills = [skill_value for skill_value in dict(employee_skills).values() if skill_value is not None]
            average_rating = sum(rated_skills) / len(rated_skills) if rated_skills else 0
        else:
            total_skills_rated = 0
            average_rating = 0

        employees_with_skills.append({
            "user_id": employee.user_id,
            "name": employee.name,
            "designation": employee.designation,
            "account": employee.account,
            "lead": employee.lead,
            "manager_name": employee.manager_name,
            "skills": employee_skills,
            "total_skills_rated": total_skills_rated,
            "average_rating": average_rating
        })

    return employees_with_skills

@router.get("/sme_finder/")
async def sme_finder(
    db: Session = Depends(deps.get_db),
    name: Optional[str] = Query(None, description="Filter by employee name"),
    designation: Optional[str] = Query(None, description="Filter by employee designation"),
    account: Optional[str] = Query(None, description="Filter by employee account"),
    lead: Optional[str] = Query(None, description="Filter by employee lead"),
    manager_name: Optional[str] = Query(None, description="Filter by employee manager name"),
    validated: Optional[str] = Query(None, description="Filter by validated or not-validated"),
    skills: Optional[str] = Query(None, description="Filter by skill name"),
    rating: Optional[int] = Query(None, description="Filter by skill rating")
):
    # Base query for employees
    employees_query = db.query(employeeModel)

    # Apply filters for employees
    if name is not None:
        employees_query = employees_query.filter(employeeModel.name == name)
    if designation is not None:
        employees_query = employees_query.filter(employeeModel.designation == designation)
    if account is not None:
        employees_query = employees_query.filter(employeeModel.account == account)
    if lead is not None:
        employees_query = employees_query.filter(employeeModel.lead == lead)
    if manager_name is not None:
        employees_query = employees_query.filter(employeeModel.manager_name == manager_name)
    if validated is not None:
        employees_query = employees_query.filter(employeeModel.latest == validated)
    
    # Base query for skills
    skills_query = db.query(Skills1)

    if skills is not None and rating is not None:
        # Assuming skills are filtered based on the lowercase version of their names
        skill_column = getattr(Skills1, skills.lower(), None)
        if skill_column is not None:
            skills_query = skills_query.filter(skill_column == rating)
    if skills is not None and rating is None:
        skill_column = getattr(Skills1,skills.lower(),None)
        if skill_column is not None:
            skills_query = skills_query.filter(skill_column.isnot(None))
    if skills is None and rating is not None:
        # Construct OR condition for all columns of Skills1
        or_conditions = []
        for column in Skills1.__table__.columns:
            if column.name != 'user_id':  # Exclude user_id column from filtering
                or_conditions.append(column == rating)
        
        # Apply the OR conditions to the query
        skills_query = skills_query.filter(or_(*or_conditions))
    # Fetch the skills
    skills = skills_query.all()
    # Fetch the skills
    skills = skills_query.all()

    # Create a map from user_id to skills
    skills_map = {}
    for skill in skills:
        if skill.user_id not in skills_map:
            skills_map[skill.user_id] = SkillBase(
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
            )

    user_ids = list(skills_map.keys())

    # Query employees with the filtered user_ids
    employees_query = employees_query.filter(employeeModel.user_id.in_(user_ids))
    employees = employees_query.all()

    if not employees:
        raise HTTPException(status_code=404, detail="Employee(s) not found")

    # Create employees with skills and calculate total_skills_rated and average_rating
    employees_with_skills = []
    for employee in employees:
        employee_skills = skills_map.get(employee.user_id)
        
        employees_with_skills.append({
            "user_id": employee.user_id,
            "name": employee.name,
            "designation": employee.designation,
            "account": employee.account,
            "lead": employee.lead,
            "manager_name": employee.manager_name,
            "validated": employee.latest,
            "skills": employee_skills
        })

    return employees_with_skills
# @router.get("/search/", status_code=200, response_model=employeeSearchResults)
# def search_employees(
#     *,
#     keyword: str = Query(None, min_length=3, example="chicken"),
#     max_results: Optional[int] = 10,
#     db: Session = Depends(deps.get_db),
# ) -> dict:
#     """
#     Search for employees based on label keyword
#     """
#     employees = crud.employee.get_multi(db=db, limit=max_results)
#     results = filter(lambda employee: keyword.lower() in employee.label.lower(), employees)

#     return {"results": list(results)}

