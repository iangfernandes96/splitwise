#!/usr/bin/python3

from pydantic import BaseModel, UUID4
from typing import List


class GroupCreateSchema(BaseModel):
    name: str
    group_members: List[str]

    class Config:
        orm_mode = True


class GroupResponseSchema(BaseModel):
    id: UUID4
    name: str
    members: List[str]
    owner_email: str

    class Config:
        orm_mode = True
