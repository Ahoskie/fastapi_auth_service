from typing import List
from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.orm import Session

from schemas.user import UserGet, UserCreate, UserObtainToken, AuthenticationToken
from services.users import get_all_users, create_user, delete_user, obtain_token, verify_token
from database import get_db


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/', response_model=List[UserGet])
def list_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_all_users(db, limit, skip)


@router.post('/', response_model=UserGet)
def post_user(user: UserCreate, db: Session = Depends(get_db)):
    created_user = create_user(db, user)
    return created_user


@router.delete('/{user_id}/')
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    delete_user(db, user_id)
    return Response(status_code=204)


@router.post('/obtain-token/')
def obtain_token_by_user_id(user: UserObtainToken, db: Session = Depends(get_db)):
    access_token = obtain_token(db, user)
    response_data = AuthenticationToken(access_token=access_token)
    return response_data


@router.post('/verify-token/')
def post_verify_token(token: AuthenticationToken, db: Session = Depends(get_db)):
    verify_token(db, token)
    return Response(status_code=200)
