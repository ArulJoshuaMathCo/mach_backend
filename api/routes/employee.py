from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.Employee import MACH_Employee as employeeModel
import crud
from api import deps
from models.user import User
from schemas.employee import EmployeeCreate, MACH_Employee
from sqlalchemy.future import select
from typing import List
from schemas.employee import MACH_Employee,employeeSearchResults
from schemas.replacement_finder import ReplacementFinderResponse
from schemas.talent_finder import TalentFinder
from schemas.executive_sumary import ExecutiveSummary
from services.service import *
from services.replacement_service import *
from services.employee_skill_screen import *

router = APIRouter()

from sqlalchemy import select, join
@router.get("/talent_finder/",response_model=List[TalentFinder])
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
    current_user: User = Depends(deps.get_current_user),
    # page: int = Query(1, description="Page number"),
    # page_size: int = Query(10, description="Number of items per page")
):
    rows =await fetch_employees(
        db, name, designation, account, lead, manager_name, validated,tenure,iteration,capabilities,serviceline_name,functions, skill_name, rating,
        
    )
    employees_with_skills = await process_employees_with_skills1(rows,rating,skill_name)
    return employees_with_skills

@router.get("/replacement_finder/",response_model=ReplacementFinderResponse)
async def replacement_finder(
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
    current_user: User = Depends(deps.get_current_user),
):
    rows = await fetch_employees(db, name,)    
    user_ids = [employee.user_id for employee in rows]
    # Calculate average skill ratings
    skill_avg_ratings = await calculate_skill_avg_ratings(db, user_ids,skill_name)
    if not skill_avg_ratings:
        raise HTTPException(status_code=404, detail="No skill ratings found")
    employees= await fetch_employees(db,designation=designation, account=account,validated=validated,lead=lead,manager_name=manager_name,tenure=tenure,iteration=iteration,capabilities=capabilities,serviceline_name=serviceline_name,function=functions ,skill_name=skill_name,rating=rating,)    
    employees_with_skills = await process_employees_with_skills1(employees,rating=rating,skill_query_name=skill_name)
    overall_avg_rating = await calculate_overall_avg_rating(skill_avg_ratings)
    nearest_matches = await find_nearest_matches(employees_with_skills, overall_avg_rating,skill_avg_rating=skill_avg_ratings,name=name)
    
    return {
        "skill_avg_ratings": skill_avg_ratings,
        "overall_average_rating": overall_avg_rating,
        "nearest_matches": nearest_matches
    }
from schemas.employee_skill_screen import EmployeeSkillScreen, EmployeeSkill

@router.get("/employees_skill_screen/")
async def employees_skill_screen(
    db: AsyncSession = Depends(deps.get_db),
    serviceline_name: Optional[List[str]] = Query(None, description="Filter by serviceline"),
    lead: Optional[List[str]] = Query(None, description="Filter by lead"),
    manager_name: Optional[List[str]] = Query(None, description="Filter by manager"),
    capabilities: Optional[List[str]] = Query(None, description="Filter by capabilities"),
    designation: Optional[List[str]] = Query(None, description="Filter by designation"),
    validated: Optional[List[str]] = Query(None, description="Filter by validation"),
    iteration: Optional[List[str]] = Query(None, description="Filter by iteration"),
    rating: Optional[List[int]] = Query(None, description="Filter by rating"),
    name: Optional[List[str]] = Query(None, description="Filter by employee name"),
    account: Optional[List[str]] = Query(None, description="Filter by employee account"),
    current_user: User = Depends(deps.get_current_user)
):
    
    rows =await fetch_employees(db, serviceline_name=serviceline_name, lead=lead, manager_name=manager_name, capabilities=capabilities, designation=designation, validated=validated, iteration=iteration, rating=rating, name=name, account=account,)
    user_ids = [employee.user_id for employee in rows]
    
    skill_avg_rating = await calculate_skill_avg_ratings(db, user_ids)
    skill_avg_ratings = await calculate_skill_avg_ratings_with_counts(db, user_ids)
    if not skill_avg_ratings:
        raise HTTPException(status_code=404, detail="No skill ratings found")
    
    overall_avg_rating = await calculate_overall_avg_rating(skill_avg_rating)
    number_of_people = len(set(user_ids))
   
    return [{
        "overall_average": overall_avg_rating,
        "number_of_people": number_of_people,
        "skill_avg_ratings": skill_avg_ratings,
    }]

@router.get("/executive_summary/")
async def executive_summary(
    db: AsyncSession = Depends(deps.get_db),
    serviceline_name: Optional[List[str]] = Query(None, description="Filter by serviceline"),
    skill_name: Optional[List[str]] = Query(None, description="Filter by skill name"),
    current_user: User = Depends(deps.get_current_user)
):
    if skill_name and not serviceline_name:
        raise HTTPException(status_code=400, detail="Must provide serviceline_name when filtering by skill_name")

    rows =await fetch_employees(db, serviceline_name=serviceline_name, skill_name=skill_name)
    user_ids = [employee.user_id for employee in rows]
    skill_avg_rating = await calculate_skill_avg_ratings(db, user_ids, skill_names=skill_name)
    skill_avg_ratings = await calculate_skill_avg_ratings_with_count(db, user_ids, skill_names=skill_name)
    if not skill_avg_ratings:
        raise HTTPException(status_code=404, detail="No skill ratings found")
    service_line_skill_percentages = await fetch_service_line_percentages(db, user_ids, skill_names=skill_name)
    service_line_percentages = await fetch_service_line_percentage(db, user_ids, skill_names=skill_name)
    overall_avg_rating = await calculate_overall_avg_rating(skill_avg_rating)
    number_of_people = len(set(user_ids))

    return {
        "service_line_percentage": service_line_percentages,
        "service_line_skill_percentages": service_line_skill_percentages,
        "overall_average": overall_avg_rating,
        "total_number_of_people": number_of_people,
        "skill_avg_ratings": skill_avg_ratings
    }


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

@router.get("/designation-count/")
async def get_designation_counts(
    account: Optional[str] = Query(None, description="Filter by account name"),
    manager_name: Optional[str] = Query(None, description="Filter by manager name"),
    name:Optional[str] = Query(None, description="Filter by name"),
    lead:Optional[str] = Query(None, description="Filter by lead"),
    serviceline_name:Optional[str] = Query(None, description="Filter by serviceline"),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
   
    query = select(
        employeeModel.designation,
        func.count(employeeModel.designation)
    ).group_by(employeeModel.designation)

    if account:
        query = query.where(employeeModel.account == account)
    if manager_name:
        query = query.where(employeeModel.manager_name == manager_name)
    if name:
        query = query.where(employeeModel.name == name)
    if lead:
        query = query.where(employeeModel.lead == lead)
    if serviceline_name:
        query = query.where(employeeModel.serviceline_name == serviceline_name)

    result = db.execute(query)
    designation_counts = result.fetchall()

    total_count_query = select(func.count()).select_from(employeeModel)

    if account:
        total_count_query = total_count_query.where(employeeModel.account == account)
    if manager_name:
        total_count_query = total_count_query.where(employeeModel.manager_name == manager_name)
    if name:
        total_count_query = total_count_query.where(employeeModel.name == name)
    if lead:
        total_count_query = total_count_query.where(employeeModel.lead == lead)
    if serviceline_name:
        total_count_query = total_count_query.where(employeeModel.serviceline_name == serviceline_name)

    total_count_result = db.execute(total_count_query)
    total_count = total_count_result.scalar()

    formatted_counts = [
        {"designation": designation, "count": count}
        for designation, count in designation_counts
    ]

    return {"designation_counts": formatted_counts,
            "total_count": total_count}