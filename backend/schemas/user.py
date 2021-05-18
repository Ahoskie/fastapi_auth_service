from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase):
    role_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    password: str


class UserGet(UserBase):
    id: int
    role: str
    is_active: bool


class Settings(BaseModel):
    pass
