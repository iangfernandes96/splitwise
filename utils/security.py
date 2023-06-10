#!/usr/bin/python3

from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

from utils.constants import SECRET_KEY, ACCESS_TOKEN_SECONDS, ALGORITHM


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:  # noqa
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_SECONDS)
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
