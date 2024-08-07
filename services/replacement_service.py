from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import func, or_
from concurrent.futures import ThreadPoolExecutor
import asyncio
from decimal import Decimal
from models.Employee import MACH_Employee as employeeModel
from models.skills import Skills1
from services.service import run_in_executor

async def calculate_skill_avg_ratings(
    db: Session,
    user_ids: List[str],
    skill_names: Optional[List[str]]=None
) -> Dict[str, Decimal]:
    skill_avg_ratings = {}

    for skill_column in Skills1.__table__.columns:
        if skill_column.name != 'EMP ID':
            avg_rating_query = db.query(func.avg(skill_column)).filter(
                skill_column.isnot(None),
                Skills1.user_id.in_(user_ids)
            )

            if skill_names:
                skill_conditions = [
                    getattr(Skills1, skill_name.lower(), None).isnot(None)
                    for skill_name in skill_names if getattr(Skills1, skill_name.lower(), None) is not None
                ]
                if skill_conditions:
                    avg_rating_query = avg_rating_query.filter(or_(*skill_conditions))
            
            avg_rating = await run_in_executor(avg_rating_query.scalar)
            if avg_rating is not None:
                avg_rating = round(avg_rating, 2)
                skill_avg_ratings[skill_column.name] = avg_rating
            else:
                skill_avg_ratings[skill_column.name] = float(0)

    return skill_avg_ratings

async def find_nearest_matches(
    employees_with_skills: List[Dict[str, Any]],
    overall_avg_rating: Decimal,
    skill_avg_rating: Dict[str, float],
    name: Optional[str] = None
) -> List[Dict[str, Any]]:
    nearest_matches = []

    for employee in employees_with_skills:
        if name is None or employee['name'] not in name:
            matching_skills = 0
            match = {}
            skill_score = 0
            total_skill_ratings = 0
            matched_skill_ratings = 0

            for skill_name, skill_value in employee['skills'].items():
                mapped_skill_name = skill_name
                avg_rating = skill_avg_rating.get(mapped_skill_name, 0)

                if mapped_skill_name in skill_avg_rating.keys() and skill_value != 0 and avg_rating != 0:
                    matching_skills += 1
                    match[skill_name] = skill_value
                    total_skill_ratings += avg_rating
                    matched_skill_ratings += skill_value  # Summing the ratings of the matched skills
                    skill_score += skill_value / avg_rating

            employee['matching_skills'] = matching_skills
            employee['matched_skills'] = match

            if matching_skills > 0:
                # Calculate skill relevance
                skill_relevance = (matching_skills / len(skill_avg_rating))

                # Calculate average skill score
                average_skill_score = skill_score / matching_skills if matching_skills > 0 else 0

                # Calculate the average rating of the matched skills
                avg_matched_skill_rating = matched_skill_ratings / matching_skills if matching_skills > 0 else 0
                employee["matched_skills_avg"]= avg_matched_skill_rating if matching_skills>0 else 0
                # Check if the employee has all required skills
                has_all_skills = matching_skills == len(skill_avg_rating)
                
                # Calculate confidence score with emphasis on matching all required skills
                confidence_score = (
                    (1 if has_all_skills else 0) * 0.8 +  # High weight for having all required skills
                    skill_relevance * 0.15 +  # Medium weight for skill relevance
                    (avg_matched_skill_rating / overall_avg_rating) * 0.05  # Lower weight for matched skill ratings
                )

                employee['confidence_score'] = confidence_score * 100
                nearest_matches.append(employee)
    
    # Sort by confidence score in descending order
    nearest_matches.sort(key=lambda x: x['confidence_score'], reverse=True)
    return nearest_matches[1:11]





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

async def rf_fetch_employees(
    db: Session,
    name: Optional[List[str]] = None,
    designation: Optional[List[str]]= None,
    account: Optional[List[str]]= None,
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

async def calculate_overall_avg_rating(skill_avg_ratings: Dict[str, float]) -> float:
    # Filter out zero values
    non_zero_ratings = [rating for rating in skill_avg_ratings.values() if rating > 0]
    
    total_rating = sum(non_zero_ratings)
    total_skills = len(non_zero_ratings)

    overall_avg_rating = total_rating / total_skills if total_skills > 0 else 0
    rounded_overall_avg_rating = round(overall_avg_rating, 2)
    
    return rounded_overall_avg_rating
