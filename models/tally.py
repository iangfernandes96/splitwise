#!/usr/bin/python3
from .db import Base
from sqlalchemy import Column, Integer, Float, UUID, String
import uuid


class Tally(Base):
    __tablename__ = "tally"
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )  # noqa
    user1 = Column(String)
    user2 = Column(String)
    amount = Column(Float)
    bill_id = Column(Integer)
