#!/usr/bin/python3

from sqlalchemy.orm import Session
from models import User
from models.db import get_db
from typing import Optional, List, Union
from schemas import UserSchema
from fastapi.params import Depends
from utils.constants import (
    SECRET_KEY,
    ALGORITHM,
    oauth2_scheme,
    hash_password,
    verify_password,
)
from fastapi import HTTPException
from starlette import status
from jose import jwt, JWTError


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == id).first()

    def get_all_users(self) -> List[User]:
        return self.db.query(User).filter().all()

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def validate_members(self, group_members: list[str]) -> bool:
        group_users = [
            user
            for email in group_members
            if (
                user := UserRepository(self.db).get_user_by_email(email=email)
                is not None  # noqa
            )
        ]
        return len(group_members) == len(group_users)

    def create_user(self, user_data: UserSchema):
        hashed_password = hash_password(user_data.password)
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,  # noqa
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def authenticate_user(self, email: str, password: str) -> Union[bool, User]:  # noqa
        user: User = self.get_user_by_email(email=email)
        if not user or not verify_password(password, str(user.hashed_password)):  # noqa
            return False
        return user

    def get_current_user(
        self,
        token: str = Depends(oauth2_scheme),  # type: ignore
        db: Session = Depends(get_db),  # type: ignore
    ) -> User:
        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")  # type: ignore
            if email is None:
                raise credential_exception
        except JWTError:
            raise credential_exception
        user = UserRepository(db).get_user_by_email(email=email)
        if user is None:
            raise credential_exception
        return user
