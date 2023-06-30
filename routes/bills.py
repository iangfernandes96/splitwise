#!/usr/bin/python3

from fastapi import APIRouter, HTTPException
from typing import Optional
from schemas import BillCreateSchema, BillResponseSchema, BillUpdateSchema
from models.db import get_db
from sqlalchemy.orm import Session
from fastapi.params import Depends
from repositories import BillRepository, UserRepository
from models import Bill, User
from common import MemberValidationError
import uuid


bill_router = APIRouter()


@bill_router.get("/{bill_id:str}", response_model=BillResponseSchema)
def get_bill_by_id(bill_id: str, db: Session = Depends(get_db)) -> Optional[Bill]:  # type: ignore # noqa
    bill = BillRepository(db).get_bill_by_id(uuid.UUID(hex=bill_id))
    if not bill:
        print("bill not found")
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


@bill_router.post("", response_model=BillResponseSchema)
def create_bill(
    bill_data: BillCreateSchema,
    db: Session = Depends(get_db),  # type: ignore
    current_user: User = Depends(UserRepository(db=Depends(get_db)).get_current_user),  # type: ignore # noqa
) -> Optional[Bill]:
    try:
        bill = BillRepository(db).create_bill(
            bill_data=bill_data, user=current_user
        )  # noqa
    except MemberValidationError:
        raise HTTPException(
            status_code=400, detail="Some members are not on splitwise"
        )  # noqa
    except Exception:
        raise HTTPException(status_code=500, detail="Error creating bill")

    try:
        pass
        # create tally for bill
        # save tallies
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating tally records for bill {str(e)}",  # noqa
        )
    return bill


@bill_router.put("", response_model=BillResponseSchema)
def update_bill(
    bill_data: BillUpdateSchema,
    db: Session = Depends(get_db),  # type: ignore
    current_user: User = Depends(UserRepository(db=Depends(get_db)).get_current_user),  # type: ignore # noqa
) -> Optional[Bill]:
    bill = BillRepository(db).get_bill_by_id(bill_data.id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    try:
        bill = BillRepository(db).update_bill(
            bill_data=bill_data, user=current_user
        )  # noqa
    except MemberValidationError:
        raise HTTPException(
            status_code=400, detail="Some members are not on splitwise"
        )  # noqa
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error while updating bill {str(e)}"  # noqa
        )

    try:
        pass
        # delete exisging bill tallies
        # recompute and save updated tallies
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating tally records for bill {str(e)}",  # noqa
        )
    return bill
