#!/usr/bin/python3

from pydantic import BaseModel, UUID4
from typing import Optional


class BillCreateSchema(BaseModel):
    name: str
    amount: float
    payer: str
    owed_by: list[str]
    owner_email: str
    group_id: Optional[str] = None

    class Config:
        orm_mode = True


class BillUpdateSchema(BillCreateSchema):
    id: UUID4


class BillResponseSchema(BillUpdateSchema):
    pass
