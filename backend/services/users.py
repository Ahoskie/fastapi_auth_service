import datetime

import jwt
import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas.user import UserCreate, UserGet, UserObtainToken, AuthenticationToken
from models.user import User
from models.permissions import Role
from database.exceptions import DatabaseException, NotFoundException
from services import check_uniqueness, delete_instance
from services.exceptions import JWTException
from core.config import SECRET_KEY


def validate_user(db: Session, user):
    check_uniqueness(db, User, 'name', user.name)
    check_uniqueness(db, User, 'email', user.email)
    db_role = db.query(Role).get(user.role_id)
    if not db_role:
        raise DatabaseException(f'Role with id {user.role_id} does not exist')


def get_all_users(db: Session, limit: int = 100, offset: int = 0):
    users = db.query(User).offset(offset).limit(limit).all()
    return [user.__dict__ for user in users]


def create_user(db: Session, user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    if not user.first_name or not user.last_name:
        user.first_name = ''
        user.last_name = ''
    user.password = hashed_password.decode('utf-8')
    validate_user(db, user)
    try:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError as error:
        raise DatabaseException(error.args)
    return db_user.__dict__


def delete_user(db: Session, user_id: int):
    delete_instance(db, user_id, User)


def create_new_token(user):
    exp_time = datetime.datetime.today() + datetime.timedelta(days=1)
    decoded_user = {
        'name': user.name,
        'email': user.email,
        'sub': user.id,
        'exp': datetime.datetime.fromisoformat(exp_time.isoformat()).timestamp()
    }
    token = jwt.encode(decoded_user, SECRET_KEY, algorithm='HS256')
    return token


def obtain_token(db: Session, user: UserObtainToken):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise NotFoundException('User with the requested email was not found')
    password_is_valid = bcrypt.checkpw(user.password.encode(), db_user.password.encode())
    if not password_is_valid:
        raise DatabaseException('User email and password do not match')
    return create_new_token(db_user)


def verify_token(db: Session, token: AuthenticationToken):
    access_token = token.access_token
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')
    except jwt.exceptions.DecodeError or jwt.exceptions.InvalidSignatureError:
        raise JWTException('Bad token format')
    except jwt.exceptions.ExpiredSignatureError:
        raise JWTException('The token is expired')
    return payload
