#!/usr/bin/python3

from sqlalchemy.orm import Session
from pydantic import UUID4
from models import Bill, User
from typing import Optional
from common import MemberValidationError, UserNotAuthorizedError
from repositories import UserRepository
from schemas import BillCreateSchema, BillUpdateSchema


class BillRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_bill_by_id(self, id: UUID4) -> Optional[Bill]:
        return self.db.query(Bill).filter(Bill.id == id).first()

    def create_bill(
        self, bill_data: BillCreateSchema, user: User
    ) -> Optional[Bill]:  # noqa
        if not UserRepository(self.db).validate_members(
            bill_data.owed_by
        ) or not UserRepository(self.db).validate_members([bill_data.payer]):
            raise MemberValidationError
        bill = Bill(
            name=bill_data.name,
            amount=bill_data.amount,
            payer=bill_data.payer,
            owed_by=bill_data.owed_by,
            group_id=bill_data.group_id,
            owner_email=user.email,
            created_by=user,
        )
        self.db.add(bill)
        self.db.commit()
        self.db.refresh(bill)
        return bill

    def update_bill(
        self, bill_data: BillUpdateSchema, user: User
    ) -> Optional[Bill]:  # noqa
        if not UserRepository(self.db).validate_members(
            bill_data.owed_by
        ) or not UserRepository(self.db).validate_members([bill_data.payer]):
            raise MemberValidationError

        bill = self.db.query(Bill).filter(Bill.id == bill_data.id).first()
        if bill and str(bill.owner_email) != user.email:
            raise UserNotAuthorizedError
        for var, value in vars(bill_data).items():
            setattr(bill, var, value) if value and str(var) != "id" else None
        self.db.add(bill)
        self.db.commit()
        self.db.refresh(bill)
        return bill
