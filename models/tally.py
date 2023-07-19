#!/usr/bin/python3
from .db import Base
from sqlalchemy import Column, Float, UUID, String
import uuid


class Tally(Base):
    __tablename__ = "tally"
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )  # noqa
    payer = Column(String)
    payee = Column(String)
    amount = Column(Float)
    bill_id = Column(String)
