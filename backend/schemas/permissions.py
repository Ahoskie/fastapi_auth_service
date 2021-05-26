from typing import List, Optional

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    groups: List[int] = []

    class Config:
        orm_mode = True


class RoleGet(RoleBase):
    id: int


class RoleUpdate(BaseModel):
    name: Optional[str]
    groups: Optional[List[int]]


class GroupBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class GroupGet(GroupBase):
    id: int


class RoleGetExtendedGroups(RoleBase):
    id: int
    groups: List[GroupGet]


class GroupUpdate(BaseModel):
    name: Optional[str]
    roles: Optional[List[int]]
