from fastapi import APIRouter

from api.api_v1.endpoints import employee, auth


api_router = APIRouter()
api_router.include_router(employee.router, prefix="/mach")
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])