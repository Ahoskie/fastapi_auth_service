from fastapi import APIRouter

from api.users.users import router as users_router


api_router = APIRouter(
    prefix='/api'
)
api_router.include_router(users_router)
