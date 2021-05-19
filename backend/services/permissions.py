from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas.permissions import RoleBase, GroupBase
from models.permissions import Role, Group
from database.exceptions import DatabaseException, NotFoundException
from services import get_all, get_by_id, update_instance, delete_instance


def validate_role(db: Session, role: RoleBase):
    db_groups = db.query(Group).filter(Group.id.in_(role.groups)).all()
    if len(db_groups) < len(role.groups):
        raise NotFoundException(f'Can not find groups with ids '
                                f'"{set(role.groups) - set([group.id for group in db_groups])}" in database')
    role.groups = db_groups
    return role


def get_all_roles(db: Session, limit: int = 100, offset: int = 0):
    return get_all(db, Role, limit, offset)


def get_role_by_id(db: Session, role_id: int):
    return get_by_id(db, role_id, Role)


def create_role(db: Session, role: RoleBase):
    db_role = db.query(Role).filter(Role.name == role.name).first()
    if db_role:
        raise DatabaseException(f'Role with name {role.name} already exists')
    role = validate_role(db, role)
    try:
        db_role = Role(**role.dict())
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
    except IntegrityError as error:
        raise DatabaseException(error.args)
    return db_role


def update_role(db: Session, role_id: int, role: RoleBase):
    db_role = db.query(Role).get(role_id)
    if not db_role:
        raise NotFoundException(f'Role with id {role_id} does not exist')
    validated_model = validate_role(db, role)
    try:
        update_instance(db_role, validated_model)
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
    except IntegrityError as error:
        raise DatabaseException(error.args)
    return db_role


def delete_role(db: Session, role_id: int):
    delete_instance(db, role_id, Role)


def get_all_groups(db: Session, limit: int = 100, offset: int = 0):
    return get_all(db, Group, limit, offset)


def get_group_by_id(db: Session, group_id: int):
    return get_by_id(db, group_id, Group)


def create_group(db: Session, group: GroupBase):
    db_group = db.query(Group).filter(Group.name == group.name).first()
    if db_group:
        raise DatabaseException(f'Group with name {group.name} already exists')
    try:
        db_group = Group(**group.dict())
        db.add(db_group)
        db.commit()
        db.refresh(db_group)
    except IntegrityError as error:
        raise DatabaseException(error.args)
    return db_group


def update_group(db: Session, group_id: int, group: GroupBase):
    db_group = db.query(Group).get(group_id)
    if not db_group:
        raise NotFoundException(f'Group with id {group_id} does not exist')
    try:
        update_instance(db_group, group)
        db.add(db_group)
        db.commit()
        db.refresh(db_group)
    except IntegrityError as error:
        raise DatabaseException(error.args)
    return db_group


def delete_group(db: Session, group_id: int):
    delete_instance(db, group_id, Group)

