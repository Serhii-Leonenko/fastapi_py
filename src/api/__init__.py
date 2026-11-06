from fastapi import APIRouter

from . import v1


api_v1_router = APIRouter()
api_v1_router.include_router(v1.user_router)
api_v1_router.include_router(v1.project_router)


__all__ = ["api_v1_router"]
