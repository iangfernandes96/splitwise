#!/usr/bin/python3

from sqlalchemy.orm import Session
from models import Tally, Bill
from schemas import TallyCreateSchema
from typing import Optional


class TallyRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_tally_by_payer(self, email: str) -> Optional[list[Tally]]:
        return self.db.query(Tally).filter(Tally.payer == email).all()

    def get_tally_by_payee(self, email: str) -> Optional[list[Tally]]:
        return self.db.query(Tally).filter(Tally.payee == email).all()

    def get_tally_by_bill_id(self, bill_id: str) -> Optional[list[Tally]]:
        return self.db.query(Tally).filter(Tally.bill_id == bill_id).all()

    def create_tally(self, tally_data: TallyCreateSchema) -> Optional[Tally]:
        tally = Tally(
            payer=tally_data.payer,
            payee=tally_data.payee,
            amount=tally_data.amount,
            bill_id=tally_data.bill_id,
        )
        self.db.add(tally)
        self.db.commit()
        self.db.refresh(tally)
        return tally

    def bill_to_tally(self, bill: Bill) -> Optional[list[Tally]]:  # noqa
        bill_members = len(bill.owed_by)  # type: ignore
        payer = bill.payer
        tally_record_data = [
            TallyCreateSchema(
                payer=payer,  # type: ignore
                payee=member,  # type: ignore
                amount=float(bill.amount / bill_members),  # type: ignore
                bill_id=str(bill.id),
            )
            for member in bill.owed_by
            if payer is not member
        ]
        tally_records = [
            self.create_tally(tally_record)
            for tally_record in tally_record_data  # noqa
        ]

        self.db.add_all(tally_records)
        self.db.commit()
        return tally_records

    def delete_tally_by_bill_id(self, bill_id: str) -> None:
        tally_list = self.db.query(Tally).filter(Tally.bill_id == bill_id).all()  # noqa
        _ = list(
            map(
                lambda tally: (self.db.delete(tally), self.db.commit()),
                tally_list,  # noqa
            )
        )
        return None
