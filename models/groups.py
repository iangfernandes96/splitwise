#!/usr/bin/python3

from .db import Base

from sqlalchemy import Column, String, UUID, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
import uuid


class Group(Base):
    __tablename__ = "groups"
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )  # noqa
    members = Column(ARRAY(String), nullable=False)
    name = Column(String, nullable=False)
    owner_email = Column(String, ForeignKey("users.email"))
    owner = relationship("User", backref="groups")
