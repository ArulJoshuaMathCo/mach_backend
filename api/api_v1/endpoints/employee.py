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
from sqlalchemy import and_, or_, func
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
    skill_name: Optional[str] = Query(None, description="Filter by skill name"),
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
    # Fetch the skills
    skills = skills_query.all()

    # Create a map from user_id to skills
    skills_map = {}
    for skill in skills:
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

    user_ids = list(skills_map.keys())

    # Query employees with the filtered user_ids
    employees_query = employees_query.filter(employeeModel.user_id.in_(user_ids))
    employees = employees_query.all()

    if not employees:
        raise HTTPException(status_code=404, detail="Employee(s) not found")

    # Create employees with skills and calculate total_skills_rated and average_rating
    employees_with_skills = []
    for employee in employees:
        employee_skills = skills_map.get(employee.user_id, [])

        # Filter out skills with None values
        filtered_skills = [
            skill.dict(exclude_unset=True) for skill in employee_skills if any(value is not None for value in skill.dict().values())
        ]

        total_skills_rated = sum(len(skill) for skill in filtered_skills)
        average_rating = (sum(
            value for skill in filtered_skills for value in skill.values() if value is not None
        ) / total_skills_rated) if total_skills_rated > 0 else 0
        if len(filtered_skills) !=0 or rating is None:
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
       
@router.get("/sme_finder/")
async def sme_finder(
    db: Session = Depends(deps.get_db),
    name: Optional[str] = Query(None, description="Filter by employee name"),
    designation: Optional[str] = Query(None, description="Filter by employee designation"),
    account: Optional[str] = Query(None, description="Filter by employee account"),
    lead: Optional[str] = Query(None, description="Filter by employee lead"),
    manager_name: Optional[str] = Query(None, description="Filter by employee manager name"),
    validated: Optional[str] = Query(None, description="Filter by validated or not-validated"),
    skill_name: Optional[str] = Query(None, description="Filter by skill name"),
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

    user_ids = list(skills_map.keys())

    # Query employees with the filtered user_ids
    employees_query = employees_query.filter(employeeModel.user_id.in_(user_ids))
    employees = employees_query.all()

    if not employees:
        raise HTTPException(status_code=404, detail="Employee(s) not found")

    # Create employees with skills and calculate total_skills_rated and average_rating
    employees_with_skills = []
    for employee in employees:
        employee_skills = skills_map.get(employee.user_id, [])

        # Filter out skills with None values
        filtered_skills = [
            skill.dict(exclude_unset=True) for skill in employee_skills if any(value is not None for value in skill.dict().values())
        ]
        if len(filtered_skills) !=0 or rating is None:
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

@router.get("/replacement_finder/")
async def replacement_finder(
    db: Session = Depends(deps.get_db),
    name: Optional[str] = Query(None, description="Filter by employee name"),
    designation: Optional[str] = Query(None, description="Filter by employee designation"),
    account: Optional[str] = Query(None, description="Filter by employee account"),
    validated: Optional[str] = Query(None, description="Filter by validated or not-validated"),
    skill_name: Optional[str] = Query(None, description="Filter by skill name"),
    rating: Optional[int] = Query(None, description="Filter by skill rating")
):
    # Step 1: Filter Employees
    employees_query = db.query(employeeModel)
    if name:
        employees_query = employees_query.filter(employeeModel.name.ilike(f"%{name}%"))
    if designation:
        employees_query = employees_query.filter(employeeModel.designation.ilike(f"%{designation}%"))
    if account:
        employees_query = employees_query.filter(employeeModel.account.ilike(f"%{account}%"))
    if validated:
        employees_query = employees_query.filter(employeeModel.latest == validated)
    
    employees = employees_query.all()
    if not employees:
        raise HTTPException(status_code=404, detail="Employee(s) not found")

    # Step 2: Filter Skills
    skills_query = db.query(Skills1)
    if skill_name:
        skill_column = getattr(Skills1, skill_name.lower(), None)
        if skill_column is not None:
            if rating is not None:
                skills_query = skills_query.filter(skill_column == rating)
            else:
                skills_query = skills_query.filter(skill_column.isnot(None))
    
    skills = skills_query.all()

    # Step 3: Calculate Average Ratings for each employee
    skills_map = {}
    for skill in skills:
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

    user_ids = list(skills_map.keys())
    employees_query = db.query(employeeModel).filter(employeeModel.user_id.in_(user_ids))

    employees = employees_query.all()
    if not employees:
        raise HTTPException(status_code=404, detail="Employee(s) not found")

    employees_with_skills = []
    for employee in employees:
        employee_skills = skills_map.get(employee.user_id, [])
        filtered_skills = [
            {k: v for k, v in skill.dict().items() if v is not None} for skill in employee_skills
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

    # Step 4: Find the Nearest Match
    selected_employee = employees_with_skills[0]  # Assuming the first employee is the selected one
    selected_avg_rating = selected_employee['average_rating']

    nearest_matches = []
    for employee in employees_with_skills:
        if employee['average_rating'] >= selected_avg_rating:
            matching_skills = len(set(skill_name for skill in employee['skills'] for skill_name in skill.keys()))
            employee['matching_skills'] = matching_skills
            nearest_matches.append(employee)

    # Step 5: Calculate average rating for each skill
    skill_avg_ratings = {}
    for skill_column in Skills1.__table__.columns:
        if skill_column.name != 'user_id':
            avg_rating = db.query(func.avg(skill_column)).scalar()
            skill_avg_ratings[skill_column.name] = avg_rating

    return {
        "skill_avg_ratings": skill_avg_ratings,
        "nearest_matches": nearest_matches
    }
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

