from typing import List, Optional

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    groups: List[int] = []


class RoleGet(RoleBase):
    id: int


class RoleUpdate(BaseModel):
    name: Optional[str]
    groups: Optional[List[int]]


class GroupBase(BaseModel):
    name: str
    roles: List[int] = []


class GroupGet(GroupBase):
    id: int


class GroupUpdate(BaseModel):
    name: Optional[str]
    roles: Optional[List[int]]
