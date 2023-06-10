#!/usr/bin/python3

from fastapi import APIRouter, HTTPException
from typing import Optional
from schemas import (
    UserCreateSchema,
    TokenSchema,
    UserResponseSchema,
)  # noqa
from sqlalchemy.orm import Session
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.db import get_db
from repositories import UserRepository
from models import User
from utils.constants import ACCESS_TOKEN_SECONDS
from utils.security import create_access_token
from starlette import status
from datetime import timedelta

user_router = APIRouter()


@user_router.get("", response_model=UserResponseSchema)
def get_current_user(
    user_data: User = Depends(UserRepository(db=Depends(get_db)).get_current_user),  # type: ignore # noqa
):
    return user_data


@user_router.get("/{email:str}", response_model=UserResponseSchema)
def get_user_by_email(email: str, db: Session = Depends(get_db)) -> Optional[User]:  # type: ignore # noqa
    user = UserRepository(db).get_user_by_email(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User Not found")
    return user


@user_router.post("", response_model=UserResponseSchema)
def signup(user_data: UserCreateSchema, db: Session = Depends(get_db)) -> Optional[User]:  # type: ignore # noqa
    user = UserRepository(db).get_user_by_email(email=user_data.email)
    if user:
        raise HTTPException(status_code=409, detail="email exists")
    new_user = UserRepository(db).create_user(user_data=user_data)
    return new_user


@user_router.post("/login", response_model=TokenSchema)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()  # type: ignore # noqa
):
    user_data = UserRepository(db).authenticate_user(
        email=form_data.username, password=form_data.password
    )
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_expires_data = timedelta(seconds=ACCESS_TOKEN_SECONDS)
    access_token = create_access_token(
        data={"sub": user_data.email}, expires_delta=token_expires_data  # type: ignore # noqa
    )
    return {"access_token": access_token, "token_type": "Bearer"}
