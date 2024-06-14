from fastapi import APIRouter

from api.api_v1.endpoints import employee


api_router = APIRouter()
api_router.include_router(employee.router, prefix="/mach")