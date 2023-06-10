import os

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

SECRET_KEY = os.environ.get("SECRET_KEY") or "TOP_SECRET_KEY"
ALGORITHM = os.environ.get("ALGORITHM") or "HS256"
ACCESS_TOKEN_SECONDS = 300
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
