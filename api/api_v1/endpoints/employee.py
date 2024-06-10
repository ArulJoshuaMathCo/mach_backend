import asyncio
from typing import Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from models.Employee import MACH_Employee as employeeModel
import crud
import deps
from schemas.employee import EmployeeCreate
from sqlalchemy import and_, or_
from typing import List
from schemas.employee import MACH_Employee
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

