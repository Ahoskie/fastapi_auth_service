from sqlalchemy.orm import Session
import bcrypt

from schemas import user as user_schemas
from models import user as models_user


def get_all_users(db: Session, limit: int = 100, offset: int = 0):
    users = db.query(models_user.User).offset(offset).limit(limit).all()
    return users


def create_user(db: Session, user: user_schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    if not user.first_name or not user.last_name:
        user.first_name = ''
        user.last_name = ''
    user.password = hashed_password
    db_user = models_user.User(user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(user_id):
    return {'user': user_id, 'name': 'Work', 'age': 3, 'language': 'Python'}
