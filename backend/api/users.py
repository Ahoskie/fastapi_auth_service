import json
from typing import List
from fastapi import APIRouter, HTTPException, Response, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from schemas.user import UserGet, UserCreate, UserObtainToken, TokensGet, TokenPass, UserUpdate
from services.users import (get_all_users, create_user, delete_user, obtain_token, verify_token, refresh_access_token,
                            update_user, get_user_by_id)
from database import get_db


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/', response_model=List[UserGet])
def list_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_all_users(db, limit, skip)


@router.get('/{user_id}/', response_model=UserGet)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)


@router.post('/', response_model=UserGet)
def post_user(user: UserCreate, db: Session = Depends(get_db)):
    created_user = create_user(db, user)
    return created_user


@router.delete('/{user_id}/')
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    delete_user(db, user_id)
    return Response(status_code=204)


@router.patch('/{user_id}/', response_model=UserGet)
def patch_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user)


@router.post('/obtain-token/', response_model=TokensGet)
def obtain_token_by_user_id(user: UserObtainToken, db: Session = Depends(get_db)):
    tokens = obtain_token(db, user)
    response_data = TokensGet(**tokens)
    return response_data


@router.post('/verify-token/', response_model=UserGet)
def post_verify_token(token: TokenPass, db: Session = Depends(get_db)):
    payload = verify_token(db, token)
    return JSONResponse(payload, status_code=200)


@router.post('/refresh-token/', response_model=TokensGet)
def post_refresh_token(token: TokenPass, db: Session = Depends(get_db)):
    return TokensGet(**refresh_access_token(db, token))
