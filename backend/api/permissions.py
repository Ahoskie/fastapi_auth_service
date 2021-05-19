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
    return get_role_by_id(db, role_id)


@router.post('/roles/')
def post_role(role: RoleBase, db: Session = Depends(get_db)):
    created_role = create_role(db, role)
    return created_role


@router.patch('/roles/{role_id}/')
def patch_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    return update_role(db, role_id, role)


@router.delete('/roles/{role_id}/')
def remove_role(role_id: int, db: Session = Depends(get_db)):
    delete_role(db, role_id)
    return Response(status_code=204)


@router.get('/groups/')
def list_groups(db: Session = Depends(get_db), limit: int = 100, skip: int = 0):
    return get_all_groups(db, limit, skip)


@router.get('/groups/{group_id}/')
def get_group(group_id: int, db: Session = Depends(get_db)):
    return get_group_by_id(db, group_id)


@router.post('/groups/')
def post_group(group: GroupBase, db: Session = Depends(get_db)):
    created_group = create_group(db, group)
    return created_group


@router.patch('/groups/{group_id}/')
def patch_group(group_id: int, group: GroupUpdate, db: Session = Depends(get_db)):
    return update_role(db, group_id, group)


@router.delete('/groups/{group_id}/')
def remove_role(group_id: int, db: Session = Depends(get_db)):
    delete_group(db, group_id)
    return Response(status_code=204)
