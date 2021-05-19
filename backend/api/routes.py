from fastapi import APIRouter

from api.users import router as users_router
from api.permissions import router as permissions_router


api_router = APIRouter(
    prefix='/api'
)
api_router.include_router(users_router)
api_router.include_router(permissions_router)
