from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.exceptions import DatabaseException


def get_all(db: Session, model, limit: int = 100, offset: int = 0):
    instances = db.query(model).offset(offset).limit(limit).all()
    return instances


def get_by_id(db: Session, instance_id: int, model):
    instance = db.query(model).get(instance_id)
    if not instance:
        raise DatabaseException(f'Can not find entity with {instance_id} id')
    return instance


def update_instance(instance, model: BaseModel):
    for attr in model.dict():
        if hasattr(instance, attr) and getattr(model, attr) is not None:
            setattr(instance, attr, getattr(model, attr))


def delete_instance(db: Session, instance_id: int, model):
    instance = db.query(model).get(instance_id)
    if not instance:
        raise DatabaseException(f'Can not find entity with {instance_id} id')
    db.delete(instance)
    db.commit()
