#!/usr/bin/python3
from .db import Base
from sqlalchemy import Column, String, UUID
import uuid


class User(Base):
    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )  # noqa
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
