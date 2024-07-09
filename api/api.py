from fastapi import APIRouter

from api.routes import employee, auth, employee_management


api_router = APIRouter()
api_router.include_router(employee.router, prefix="/mach",tags=["Employee360 Screen"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(employee_management.router, prefix="/mach", tags=["Employee Management"])