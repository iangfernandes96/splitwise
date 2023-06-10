#!/usr/bin/python3

from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


class UserResponseSchema(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class UserCreateSchema(UserSchema):
    class Config:
        orm_mode = False
