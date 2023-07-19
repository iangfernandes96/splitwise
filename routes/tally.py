#!/usr/bin/python3

from fastapi import APIRouter, HTTPException
from typing import Optional
from schemas import TallyResponseSchema
from models.db import get_db
from sqlalchemy.orm import Session
from fastapi.params import Depends
from repositories import TallyRepository
from models import Tally
from collections import defaultdict


tally_router = APIRouter()


@tally_router.get(
    "/bill/{bill_id:str}", response_model=list[TallyResponseSchema]
)  # noqa
def get_tally_by_bill_id(bill_id: str, db: Session = Depends(get_db)) -> Optional[list[Tally]]:  # type: ignore # noqa
    tally_list = TallyRepository(db).get_tally_by_bill_id(bill_id)
    if not tally_list:
        raise HTTPException(
            status_code=404, detail="No tally records not found"
        )  # noqa
    return tally_list


@tally_router.get("/user/{email:str}", response_model=None)
def get_tally_for_user(email: str, db: Session = Depends(get_db)) -> Optional[list[Tally]]:  # type: ignore # noqa
    """
    Scenarios for tallying

    Bill is split such that payer is the person owed,
    payee is the person who owes. So amount will always be positive

    """

    def aggregate_tallies(
        tally_record: Optional[list[Tally]], user_email: str, owed: bool
    ) -> defaultdict[str, float]:
        def is_not_self_record(record: Tally, user_email: str) -> bool:
            return record.payee != user_email  # type: ignore

        agg_tally = defaultdict(float)
        if tally_record:
            for record in tally_record:
                if is_not_self_record(record, user_email):
                    if owed:
                        agg_tally[record.payee] += record.amount  # type: ignore # noqa
                    else:
                        agg_tally[record.payer] += record.amount  # type: ignore # noqa
        return agg_tally

    def fetch_tallies_where_user_is_owed(db: Session):
        user_is_owed = TallyRepository(db).get_tally_by_payer(email=email)
        if user_is_owed:
            return aggregate_tallies(user_is_owed, email, True)

    def fetch_tallies_where_user_owes(db: Session):
        user_owes = TallyRepository(db).get_tally_by_payee(email=email)
        if user_owes:
            return aggregate_tallies(user_owes, email, False)

    user_is_owed = fetch_tallies_where_user_is_owed(db)
    print("tally where user is owed", user_is_owed)

    user_owes = fetch_tallies_where_user_owes(db)
    print("tally where user owes", user_owes)
    return None
