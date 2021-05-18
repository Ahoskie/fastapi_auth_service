from typing import List

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    groups: List[int]


class RoleGet(RoleBase):
    id: int


class GroupBase(BaseModel):
    name: str
    roles: List[int]


class GroupGet(GroupBase):
    id: int
