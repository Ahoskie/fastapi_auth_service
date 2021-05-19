from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''
    email: EmailStr
    role_id: int


class UserCreate(UserBase):
    password: str


class UserGet(UserBase):
    id: int
    is_active: bool


class UserObtainToken(BaseModel):
    email: EmailStr
    password: str


class AuthenticationToken(BaseModel):
    access_token: str


class Settings(BaseModel):
    pass
