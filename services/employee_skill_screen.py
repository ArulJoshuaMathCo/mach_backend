from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, or_
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
import asyncio
from services.replacement_service import calculate_skill_avg_ratings
from models.skills import Skills1
from services.service import run_in_executor

async def calculate_skill_avg_ratings_with_counts(
    db: Session,
    user_ids: List[str],
    skill_names: Optional[List[str]] = None
) -> List[Dict[str, Optional[float]]]:
    skill_avg_ratings = await calculate_skill_avg_ratings(db, user_ids, skill_names)

    skill_avg_ratings_with_counts = []

    for skill_column in Skills1.__table__.columns:
        if skill_column.name != 'EMP ID':
            employee_count_query = db.query(func.count(skill_column)).filter(
                skill_column.isnot(None),
                Skills1.user_id.in_(user_ids),
                skill_column.in_([1, 2, 3, 4, 5])
            )

            if skill_names:
                skill_conditions = [
                    getattr(Skills1, skill_name.lower(), None).isnot(None)
                    for skill_name in skill_names if getattr(Skills1, skill_name.lower(), None) is not None
                ]
                if skill_conditions:
                    employee_count_query = employee_count_query.filter(or_(*skill_conditions))
            
            employee_count = await run_in_executor(employee_count_query.scalar)
            if skill_avg_ratings[skill_column.name] is not None:
                skill_avg_ratings_with_counts.append({
                    "skill_name": skill_column.name,
                    "average_rating": skill_avg_ratings[skill_column.name],
                    "employee_count": employee_count
                })
            else:
                skill_avg_ratings_with_counts.append({
                    "skill_name": skill_column.name,
                    "average_rating": None,
                    "employee_count": 0
                })

    return skill_avg_ratings_with_counts