from typing import Optional

from pydantic import BaseModel, EmailStr

from schemas.permissions import RoleGetExtendedGroups


class UserBase(BaseModel):
    name: str
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    role_id: int
    password: str


class UserUpdate(UserBase):
	name: Optional[str]
	email: Optional[EmailStr]
	role_id: Optional[int]
	is_active: Optional[bool]


class UserGet(UserBase):
    id: int
    is_active: bool
    role: RoleGetExtendedGroups


class UserObtainToken(BaseModel):
    email: EmailStr
    password: str


class TokenPass(BaseModel):
    token: str


class TokensGet(BaseModel):
    access_token: str
    refresh_token: str


class Settings(BaseModel):
    pass
