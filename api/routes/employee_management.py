from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from models.user import User
import crud
from api import deps
from schemas.employee import EmployeeCreate, MACH_Employee

router = APIRouter()

@router.post("/", status_code=201, response_model=MACH_Employee)
async def create_employee(
    *,
    employee_in: EmployeeCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_manager),
) -> dict:
    """
    Create a new employee in the database.
    """
    employee_data = employee_in.dict(exclude={'skills'})
    employee = await crud.employee.create(db=db, obj_in=employee_data)
    
    # If skills data is provided, create the Skills1 record
    if employee_in.skills:
        skills_data = employee_in.skills
        skills_data['user_id'] = employee.user_id
        await crud.skills.create(db=db, obj_in=skills_data)

    return employee

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

@router.put("/", status_code=201)
async def update_employee(
    *,
    employee_in: EmployeeCreate,
    db: Session = Depends(deps.get_current_active_manager),
) -> dict:
    """
    Update recipe in the database.
    """
    employee = await crud.employee.get(db, id=employee_in.user_id)
    if not employee:
        raise HTTPException(
            status_code=400, detail=f"employee with ID: {employee_in.user_id} not found."
        )

    update_employee = crud.employee.update(db=db, db_obj=employee, obj_in=employee_in)
    if employee_in.skills:
        skills_data = employee_in.skills
        skills_data['user_id'] = employee.user_id
        crud.skills.update(db=db, db_obj=employee.skills,obj_in=skills_data)
    db.commit()
    db.refresh(update_employee)
    return update_employee

@router.delete("/{employee_id}", status_code=204)
async def delete_employee(
    *,
    employee_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_manager)
) -> None:
    """
    Delete an employee from the database.
    """
    employee = await crud.employee.get(db, id=employee_id)
    if not employee:
        raise HTTPException(
            status_code=404, detail=f"Employee with ID: {employee_id} not found."
        )

    # Delete associated skills if necessary
    if employee.skills:
        crud.skills.remove(db=db, id=employee_id)
    
    # Delete the employee
    crud.employee.remove(db=db, id=employee_id)
    
    db.commit()
    return None