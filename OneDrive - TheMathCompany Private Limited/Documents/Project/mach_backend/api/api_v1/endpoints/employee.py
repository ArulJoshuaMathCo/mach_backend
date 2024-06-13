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

@router.get("/employees1/", response_model=List[MACH_Employee])
async def read_employees(
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


@router.get("/employees/{employee_id}", response_model=List[EmployeeWithSkills])
def read_employee(
    
    db: Session = Depends(deps.get_db),
    employee_id: Optional[UUID] = None,
    python: Optional[int] = Query(None, description="Filter by Python skill rating"),
    sql: Optional[int] = Query(None, description="Filter by SQL skill rating"),
    excel: Optional[int] = Query(None, description="Filter by Excel skill rating"),
    storyboarding: Optional[int] = Query(None, description="Filter by Storyboarding skill rating"),
    result_orientation: Optional[int] = Query(None, description="Filter by result orientation"),
    quality_focus: Optional[int] = Query(None, description="Filter by quality focus"),
    effective_communication: Optional[int] = Query(None, description="Filter by effective communication"),
    work_management_and_effectiveness: Optional[int] = Query(None, description="Filter by work management and effectiveness"),
    client_centric: Optional[int] = Query(None, description="Filter by client centric"),
    genai: Optional[int] = Query(None, description="Filter by GenAI"),
    nuclios: Optional[int] = Query(None, description="Filter by NucliOS")

):
    # Fetch the employee
    employees_query = db.query(employeeModel)

    if employee_id is not None:
        employees_query = employees_query.filter(employeeModel.user_id == employee_id)
    
    employees = employees_query.all()

    if not employees:
        raise HTTPException(status_code=404, detail="Employee(s) not found")

    # Base query for skills
    skills_query = db.query(Skills1)

    if employee_id is not None:
        skills_query = skills_query.filter(Skills1.user_id == employee_id)

    # Apply dynamic filters
    if python is not None:
        skills_query = skills_query.filter(Skills1.python == python)
    if sql is not None:
        skills_query = skills_query.filter(Skills1.sql == sql)
    if excel is not None:
        skills_query = skills_query.filter(Skills1.excel == excel)
    if storyboarding is not None:
        skills_query = skills_query.filter(Skills1.storyboarding == storyboarding)
    if result_orientation is not None:
        skills_query = skills_query.filter(Skills1.result_orientation == result_orientation)
    if quality_focus is not None:
        skills_query = skills_query.filter(Skills1.quality_focus == quality_focus)
    if effective_communication is not None:
        skills_query = skills_query.filter(Skills1.effective_communication == effective_communication)
    if work_management_and_effectiveness is not None:
        skills_query = skills_query.filter(Skills1.work_management_and_effectiveness == work_management_and_effectiveness)
    if client_centric is not None:
        skills_query = skills_query.filter(Skills1.clientcentric == client_centric)
    if genai is not None:
        skills_query = skills_query.filter(Skills1.genai == genai)
    if nuclios is not None:
        skills_query = skills_query.filter(Skills1.nuclios == nuclios)

    # Fetch the skills
    skills = skills_query.all()

    # Convert to Pydantic model
    skills_map = {}
    for skill in skills:
        if skill.user_id not in skills_map:
            skills_map[skill.user_id] = []
        skills_map[skill.user_id].append(SkillBase(
            Python=skill.python,
            SQL=skill.sql,
            Excel=skill.excel,
            Storyboarding=skill.storyboarding,
            result_orientation=skill.result_orientation,
            quality_focus=skill.quality_focus,
            effective_communication=skill.effective_communication,
            work_management_and_effectiveness=skill.work_management_and_effectiveness,
            client_centric=skill.clientcentric,
            genai=skill.genai,
            nuclios=skill.nuclios
        ))


    # Convert to Pydantic model
    employees_with_skills = [
        EmployeeWithSkills(
            user_id=employee.user_id,
            name=employee.name,
            designation=employee.designation,
            account=employee.account,
            lead=employee.lead,
            manager_name=employee.manager_name,
            skills=skills_map.get(employee.user_id, [])
        ) for employee in employees
    ]

    return employees_with_skills

@router.get("/employees/", response_model=List[EmployeeWithSkills])
def read_employees1(
    db: Session = Depends(deps.get_db),
    name: Optional[str] = Query(None, description="Filter by employee name"),
    designation: Optional[str] = Query(None, description="Filter by employee designation"),
    account: Optional[str] = Query(None, description="Filter by employee account"),
    lead: Optional[str] = Query(None, description="Filter by employee lead"),
    manager_name: Optional[str] = Query(None, description="Filter by employee manager name"),
    skills: Optional[str] = Query(None, description="Filter by Skills"),
    python: Optional[int] = Query(None, description="Filter by Python skill rating"),
    sql: Optional[int] = Query(None, description="Filter by SQL skill rating"),
    excel: Optional[int] = Query(None, description="Filter by Excel skill rating"),
    storyboarding: Optional[int] = Query(None, description="Filter by Storyboarding skill rating"),
    business_communication : Optional[int] = Query(None, description ="Filter by business communication"),
    result_orientation: Optional[int] = Query(None, description="Filter by result orientation"),
    quality_focus: Optional[int] = Query(None, description="Filter by quality focus"),
    effective_communication: Optional[int] = Query(None, description="Filter by effective communication"),
    work_management_and_effectiveness: Optional[int] = Query(None, description="Filter by work management and effectiveness"),
    client_centric: Optional[int] = Query(None, description="Filter by client centric"),
    genai: Optional[int] = Query(None, description="Filter by GenAI"),
    nuclios: Optional[int] = Query(None, description="Filter by NucliOS")
):
    # Base query for employees
    employees_query = db.query(employeeModel)

    # Apply filters for employees
      
    # Fetch the user_ids of filtered employees
    # user_ids = [employee.user_id for employee in employees]

    # Base query for skills
    skills_query = db.query(Skills1)

    if python is not None:
        skills_query = skills_query.filter(Skills1.python == python)
    if sql is not None:
        skills_query = skills_query.filter(Skills1.sql == sql)
    if excel is not None:
        skills_query = skills_query.filter(Skills1.excel == excel)
    if storyboarding is not None:
        skills_query = skills_query.filter(Skills1.storyboarding == storyboarding)
    if business_communication is not None:
        skills_query = skills_query.filter(Skills1.business_communication == business_communication)
    if result_orientation is not None:
        skills_query = skills_query.filter(Skills1.result_orientation == result_orientation)
    if quality_focus is not None:
        skills_query = skills_query.filter(Skills1.quality_focus == quality_focus)
    if effective_communication is not None:
        skills_query = skills_query.filter(Skills1.effective_communication == effective_communication)
    if work_management_and_effectiveness is not None:
        skills_query = skills_query.filter(Skills1.work_management_and_effectiveness == work_management_and_effectiveness)
    if client_centric is not None:
        skills_query = skills_query.filter(Skills1.clientcentric == client_centric)
    if genai is not None:
        skills_query = skills_query.filter(Skills1.genai == genai)
    if nuclios is not None:
        skills_query = skills_query.filter(Skills1.nuclios == nuclios)
    
    # Fetch the skills
    skills = skills_query.all()
    # print(skills)

    # Create a map from user_id to skills
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

    # Base query for employees
    employees_query = db.query(employeeModel).filter(employeeModel.user_id.in_(user_ids))

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
    
    employees = employees_query.all()

    if not employees:
        raise HTTPException(status_code=404, detail="Employee(s) not found")  

    # Convert to Pydantic model
    employees_with_skills = [
        EmployeeWithSkills(
            user_id=employee.user_id,
            name=employee.name,
            designation=employee.designation,
            account=employee.account,
            lead=employee.lead,
            manager_name=employee.manager_name,
            skills=skills_map[employee.user_id]
        ) for employee in employees
    ]

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

@router.get("/employees100/", response_model=List[EmployeeWithSkills])
def read_employees100(
    db: Session = Depends(deps.get_db),
    name: Optional[str] = Query(None, description="Filter by employee name"),
    designation: Optional[str] = Query(None, description="Filter by employee designation"),
    account: Optional[str] = Query(None, description="Filter by employee account"),
    lead: Optional[str] = Query(None, description="Filter by employee lead"),
    manager_name: Optional[str] = Query(None, description="Filter by employee manager name"),
    skills: Optional[List[str]] = Query(None, description="Filter by required skills"),
    python: Optional[int] = Query(None, description="Filter by Python skill rating"),
    sql: Optional[int] = Query(None, description="Filter by SQL skill rating"),
    excel: Optional[int] = Query(None, description="Filter by Excel skill rating"),
    storyboarding: Optional[int] = Query(None, description="Filter by Storyboarding skill rating"),
    business_communication: Optional[int] = Query(None, description="Filter by Business Communication skill rating"),
    result_orientation: Optional[int] = Query(None, description="Filter by Result Orientation skill rating"),
    quality_focus: Optional[int] = Query(None, description="Filter by Quality Focus skill rating"),
    effective_communication: Optional[int] = Query(None, description="Filter by Effective Communication skill rating"),
    work_management_and_effectiveness: Optional[int] = Query(None, description="Filter by Work Management and Effectiveness skill rating"),
    #client_centric: Optional[int] = Query(None, description="Filter by Client Centric skill rating"),
    genai: Optional[int] = Query(None, description="Filter by GenAI skill rating"),
    nuclios: Optional[int] = Query(None, description="Filter by NucliOS skill rating")
):
    employees_query = db.query(employeeModel)

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

    employee_ids = [employee.user_id for employee in employees_query.all()]

    skills_query = db.query(Skills1).filter(Skills1.user_id.in_(employee_ids))

    if python is not None:
        skills_query = skills_query.filter(Skills1.python == python)
    if sql is not None:
        skills_query = skills_query.filter(Skills1.sql == sql)
    if excel is not None:
        skills_query = skills_query.filter(Skills1.excel == excel)
    if storyboarding is not None:
        skills_query = skills_query.filter(Skills1.storyboarding == storyboarding)
    if business_communication is not None:
        skills_query = skills_query.filter(Skills1.business_communication == business_communication)
    if result_orientation is not None:
        skills_query = skills_query.filter(Skills1.result_orientation == result_orientation)
    if quality_focus is not None:
        skills_query = skills_query.filter(Skills1.quality_focus == quality_focus)
    if effective_communication is not None:
        skills_query = skills_query.filter(Skills1.effective_communication == effective_communication)
    if work_management_and_effectiveness is not None:
        skills_query = skills_query.filter(Skills1.work_management_and_effectiveness == work_management_and_effectiveness)
    #if client_centric is not None:
        #skills_query = skills_query.filter(Skills1.client_centric == client_centric)
    if genai is not None:
        skills_query = skills_query.filter(Skills1.genai == genai)
    if nuclios is not None:
        skills_query = skills_query.filter(Skills1.nuclios == nuclios)

    if skills is not None:
        for skill in skills:
            skills_query = skills_query.filter(getattr(Skills1, skill) != None)

    skills = skills_query.all()

    if not skills:
        raise HTTPException(status_code=404, detail="Skills not found for the given filters")

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
            #ClientCentric=skill.client_centric,
            GenAI=skill.genai,
            NucliOS=skill.nuclios
        ))

    user_ids = list(skills_map.keys())
    employees_query = db.query(employeeModel).filter(employeeModel.user_id.in_(user_ids))

    employees = employees_query.all()

    if not employees:
        raise HTTPException(status_code=404, detail="Employee(s) not found")

    employees_with_skills = [
        EmployeeWithSkills(
            user_id=employee.user_id,
            name=employee.name,
            designation=employee.designation,
            account=employee.account,
            lead=employee.lead,
            manager_name=employee.manager_name,
            skills=skills_map[employee.user_id]
        ) for employee in employees
    ]

    return employees_with_skills

@router.get("/employees500/", response_model=List[EmployeeWithSkills])
def read_employees500(
    db: Session = Depends(deps.get_db),
    name: Optional[str] = Query(None, description="Filter by employee name"),
    designation: Optional[str] = Query(None, description="Filter by employee designation"),
    account: Optional[str] = Query(None, description="Filter by employee account"),
    lead: Optional[str] = Query(None, description="Filter by employee lead"),
    manager_name: Optional[str] = Query(None, description="Filter by employee manager name"),
    skills: Optional[str] = Query(None, description="Comma-separated list of skills"),
    ratings: Optional[str] = Query(None, description="Comma-separated list of ratings"),
):
    employees_query = db.query(employeeModel)

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

    employee_ids = [employee.user_id for employee in employees_query.all()]

    skills_query = db.query(Skills1).filter(Skills1.user_id.in_(employee_ids))

    if skills and ratings:
        skills_list = skills.split(',')
        ratings_list = [int(rating) for rating in ratings.split(',')]
        if len(skills_list) != len(ratings_list):
            raise HTTPException(status_code=400, detail="Skills and ratings must have the same length")
        for skill, rating in zip(skills_list, ratings_list):
            skills_query = skills_query.filter(getattr(Skills1, skill.strip()) == rating)
    elif skills and not ratings:
        skills_list = skills.split(',')
        for skill in skills_list:
            skills_query = skills_query.filter(getattr(Skills1, skill.strip()) != None)

    skills = skills_query.all()

    if not skills:
        raise HTTPException(status_code=404, detail="Skills not found for the given filters")

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
            #ClientCentric=skill.client_centric,
            GenAI=skill.genai,
            NucliOS=skill.nuclios
        ))

    user_ids = list(skills_map.keys())
    employees_query = db.query(employeeModel).filter(employeeModel.user_id.in_(user_ids))

    employees = employees_query.all()

    if not employees:
        raise HTTPException(status_code=404, detail="Employee(s) not found")

    employees_with_skills = [
        EmployeeWithSkills(
            user_id=employee.user_id,
            name=employee.name,
            designation=employee.designation,
            account=employee.account,
            lead=employee.lead,
            manager_name=employee.manager_name,
            skills=skills_map[employee.user_id]
        ) for employee in employees
    ]

    return employees_with_skills

@router.get("/employees800/", response_model=List[EmployeeWithSkills])
def read_employees800(
    db: Session = Depends(deps.get_db),
    name: Optional[str] = Query(None, description="Filter by employee name"),
    designation: Optional[str] = Query(None, description="Filter by employee designation"),
    account: Optional[str] = Query(None, description="Filter by employee account"),
    lead: Optional[str] = Query(None, description="Filter by employee lead"),
    manager_name: Optional[str] = Query(None, description="Filter by employee manager name"),
    skills: Optional[str] = Query(None, description="Comma-separated list of skills"),
    ratings: Optional[str] = Query(None, description="Comma-separated list of ratings"),
):
    employees_query = db.query(employeeModel)

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

    employee_ids = [employee.user_id for employee in employees_query.all()]

    skills_query = db.query(Skills1).filter(Skills1.user_id.in_(employee_ids))

    if skills and ratings:
        skills_list = skills.split(',')
        ratings_list = [int(rating) for rating in ratings.split(',')]
        if len(skills_list) != len(ratings_list):
            raise HTTPException(status_code=400, detail="Skills and ratings must have the same length")
        for skill, rating in zip(skills_list, ratings_list):
            skills_query = skills_query.filter(getattr(Skills1, skill.strip()) == rating)
    elif skills and not ratings:
        skills_list = skills.split(',')
        for skill in skills_list:
            skills_query = skills_query.filter(getattr(Skills1, skill.strip()) > 0)  # Filter ratings > 0 for the skill

    skills = skills_query.all()

    if not skills:
        raise HTTPException(status_code=404, detail="Skills not found for the given filters")

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
            #ClientCentric=skill.client_centric,
            GenAI=skill.genai,
            NucliOS=skill.nuclios
        ))

    user_ids = list(skills_map.keys())
    employees_query = db.query(employeeModel).filter(employeeModel.user_id.in_(user_ids))

    employees = employees_query.all()

    if not employees:
        raise HTTPException(status_code=404, detail="Employee(s) not found")

    employees_with_skills = [
        EmployeeWithSkills(
            user_id=employee.user_id,
            name=employee.name,
            designation=employee.designation,
            account=employee.account,
            lead=employee.lead,
            manager_name=employee.manager_name,
            skills=skills_map[employee.user_id]
        ) for employee in employees
    ]

    return employees_with_skills
#router