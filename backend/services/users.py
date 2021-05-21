import datetime

import jwt
import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas.user import UserCreate, UserGet, UserObtainToken, TokenPass, UserUpdate
from models.user import User
from models.permissions import Role
from database.exceptions import DatabaseException, NotFoundException
from services import check_uniqueness, delete_instance, update_instance
from services.exceptions import JWTException
from core.config import SECRET_KEY, SUPERUSER_ROLE_NAME


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


def update_user(db: Session, user_id: int, user: UserUpdate):
    if user.first_name == '' or user.last_name == '':
        user.first_name = ''
        user.last_name = ''
    validate_user(db, user)
    try:
        db_user = db.query(User).get(user_id)
        if not db_user:
            raise NotFoundException(f'User with id {user_id} does not exist')
        update_instance(db_user, user)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError as error:
        raise DatabaseException(error.args)
    return db_user.__dict__


def create_new_tokens(user):
    access_exp_time = datetime.datetime.today() + datetime.timedelta(days=1)
    refresh_exp_time = datetime.datetime.today() + datetime.timedelta(days=30)
    decoded_user = {
        'name': user.name,
        'email': user.email,
        'role_id': user.role_id,
        'role_name': user.role.name,
        'sub': user.id,
        'typ': 'access',
        'exp': datetime.datetime.fromisoformat(access_exp_time.isoformat()).timestamp()
    }
    decoded_refresh = {
        'typ': 'refresh',
        'sub': user.id,
        'exp': datetime.datetime.fromisoformat(refresh_exp_time.isoformat()).timestamp()
    }
    refresh_token = jwt.encode(decoded_refresh, SECRET_KEY, algorithm='HS256')
    access_token = jwt.encode(decoded_user, SECRET_KEY, algorithm='HS256')
    return access_token, refresh_token


def obtain_token(db: Session, user: UserObtainToken):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise NotFoundException('User with the requested email was not found')
    password_is_valid = bcrypt.checkpw(user.password.encode(), db_user.password.encode())
    if not password_is_valid:
        raise DatabaseException('User email and password do not match')
    access, refresh = create_new_tokens(db_user)
    return {'access_token': access, 'refresh_token': refresh}


def refresh_access_token(db: Session, token: TokenPass):
    token = token.token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        if 'typ' not in payload or payload['typ'] != 'refresh':
            raise JWTException('Token type is not valid')
    except jwt.exceptions.DecodeError or jwt.exceptions.InvalidSignatureError:
        raise JWTException('Bad token format')
    except jwt.exceptions.ExpiredSignatureError:
        raise JWTException('The token is expired')

    user = db.query(User).get(payload['sub'])
    access, refresh = create_new_tokens(user)
    return {'access_token': access, 'refresh_token': refresh}


def verify_token(db: Session, token: TokenPass):
    access_token = token.token
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')
        user = db.query(User).get(payload['sub'])
        # if 'sub' == 0, it means that the token belongs to the role with internal permissions
        if not user and payload['role_name'] != SUPERUSER_ROLE_NAME:
            raise JWTException('User does not exist')
        if 'typ' not in payload or payload['typ'] != 'access':
            raise JWTException('Token type is not valid')
    except jwt.exceptions.DecodeError or jwt.exceptions.InvalidSignatureError:
        raise JWTException('Bad token format')
    except jwt.exceptions.ExpiredSignatureError:
        raise JWTException('The token is expired')
    return payload
