from typing import List
from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.orm import Session

from schemas.user import UserGet, UserCreate
from services.users import get_user, get_all_users, create_user
from database import get_db
from database.exceptions import DatabaseException


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/', response_model=List[UserGet])
def list_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_all_users(db, skip, limit)


@router.get('/{user_id}/')#, response_model=UserGet)
def read_user_by_id(user_id: str, db: Session = Depends(get_db)):
    return get_user(user_id)
    # try:
    #     return get_user_by_id(brand_id=brand_id)
    # except DocumentNotFound as e:
    #     raise HTTPException(status_code=404, detail=e.message)


@router.post('/', response_model=UserGet)
def post_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = create_user(db, user)
    except DatabaseException as error:
        raise HTTPException(status_code=404, detail=error.message)
    return created_user
#
#
# @router.patch('/{brand_id}/', response_model=BrandDB)
# async def patch_brand(brand_id: str, brand: BrandPartialUpdate):
#     try:
#         brand = await update_brand(brand_id, brand)
#     except DocumentNotFound as e:
#         raise HTTPException(status_code=404, detail=e.message)
#     except DocumentAlreadyExists as e:
#         raise HTTPException(status_code=400, detail=e.message)
#     return brand
#
#
# @router.delete('/{brand_id}/')
# async def delete_brand(brand_id: str):
#     try:
#         brand = await remove_brand(brand_id)
#     except DocumentNotFound as e:
#         raise HTTPException(status_code=404, detail=e.message)
#     return Response(status_code=204)
