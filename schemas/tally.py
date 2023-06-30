#!/usr/bin/python3

from pydantic import BaseModel, UUID4


class TallyCreateSchema(BaseModel):
    user1: str
    user2: str
    amount: float
    bill_id: str

    class Config:
        orm_mode = True


class TallyResponseSchema(TallyCreateSchema):
    id: UUID4
