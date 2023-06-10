#!/usr/bin/python3
from .db import Base
from sqlalchemy import Column, Float, ARRAY, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

import uuid


class Bill(Base):
    __tablename__ = "bills"
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )  # noqa
    name = Column(String)
    amount = Column(Float)
    payer = Column(String)
    owed_by = Column(ARRAY(String))
    group_id = Column(UUID(as_uuid=True), nullable=True)
    owner_email = Column(String, ForeignKey("users.email"))
    created_by = relationship("User", backref="bills")
