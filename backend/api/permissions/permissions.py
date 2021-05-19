from typing import List
from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.orm import Session

from schemas.permissions import GroupBase, RoleBase, RoleUpdate, GroupUpdate
from services.permissions import (get_all_roles, get_all_groups, create_group, create_role, get_group_by_id,
                                  get_role_by_id, update_role, delete_role, delete_group, update_group)
from database import get_db
from database.exceptions import DatabaseException


router = APIRouter(
    prefix='/permissions',
    tags=['permissions']
)


@router.get('/roles/')
def list_roles(db: Session = Depends(get_db), limit: int = 100, skip: int = 0):
    return get_all_roles(db, limit, skip)


@router.get('/roles/{role_id}/')
def get_role(role_id: int, db: Session = Depends(get_db)):
    try:
        return get_role_by_id(db, role_id)
    except DatabaseException as error:
        raise HTTPException(status_code=400, detail=error.message)


@router.post('/roles/')
def post_role(role: RoleBase, db: Session = Depends(get_db)):
    try:
        created_role = create_role(db, role)
    except DatabaseException as error:
        raise HTTPException(status_code=404, detail=error.message)
    return created_role


@router.patch('/roles/{role_id}/')
def patch_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    try:
        return update_role(db, role_id, role)
    except DatabaseException as error:
        raise HTTPException(status_code=400, detail=error.message)


@router.delete('/roles/{role_id}/')
def remove_role(role_id: int, db: Session = Depends(get_db)):
    try:
        delete_role(db, role_id)
        return Response(status_code=204)
    except DatabaseException as error:
        raise HTTPException(status_code=400, detail=error.message)


@router.get('/groups/')
def list_groups(db: Session = Depends(get_db), limit: int = 100, skip: int = 0):
    return get_all_groups(db, limit, skip)


@router.get('/groups/{group_id}/')
def get_group(group_id: int, db: Session = Depends(get_db)):
    try:
        return get_group_by_id(db, group_id)
    except DatabaseException as error:
        raise HTTPException(status_code=400, detail=error.message)


@router.post('/groups/')
def post_group(group: GroupBase, db: Session = Depends(get_db)):
    try:
        created_group = create_group(db, group)
    except DatabaseException as error:
        raise HTTPException(status_code=404, detail=error.message)
    return created_group


@router.patch('/groups/{group_id}/')
def patch_group(group_id: int, group: GroupUpdate, db: Session = Depends(get_db)):
    try:
        return update_role(db, group_id, group)
    except DatabaseException as error:
        raise HTTPException(status_code=400, detail=error.message)


@router.delete('/groups/{group_id}/')
def remove_role(group_id: int, db: Session = Depends(get_db)):
    try:
        delete_group(db, group_id)
        return Response(status_code=204)
    except DatabaseException as error:
        raise HTTPException(status_code=400, detail=error.message)
