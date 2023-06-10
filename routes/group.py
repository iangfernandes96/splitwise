#!/usr/bin/python3

from fastapi import APIRouter, HTTPException, Response
from typing import Optional
from schemas import GroupResponseSchema, GroupCreateSchema
from sqlalchemy.orm import Session
from fastapi.params import Depends
from models.db import get_db
from repositories import GroupRepository, UserRepository
from models import Group, User
from common import MemberValidationError

group_router = APIRouter()


@group_router.get("/{name:str}", response_model=GroupResponseSchema)
def get_group_by_name(name: str, db: Session = Depends(get_db)) -> Optional[Group]:  # type: ignore # noqa
    group = GroupRepository(db).get_group_by_name(name=name)
    if not group:
        raise HTTPException(status_code=404, detail="No Group with this name.")
    return group


@group_router.post("", response_model=GroupResponseSchema)
def create_group(
    group_data: GroupCreateSchema,
    current_user: User = Depends(UserRepository(db=Depends(get_db)).get_current_user),  # type: ignore # noqa
    db: Session = Depends(get_db),  # type: ignore
):
    group = GroupRepository(db).get_group_by_name(name=group_data.name)
    if group:
        raise HTTPException(
            status_code=409, detail="Group with this name exists."
        )  # noqa
    try:
        new_group = GroupRepository(db).create_group(
            group_data=group_data, current_user=current_user
        )
    except MemberValidationError:
        raise HTTPException(
            status_code=400, detail="Some members are not on Splitwise."
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong.")
    print(new_group.id)
    return new_group


@group_router.delete("", response_model=None)
def delete_group(group_data: GroupCreateSchema, db: Session = Depends(get_db)):  # type: ignore # noqa
    group = GroupRepository(db).get_group_by_name(name=group_data.name)
    if not group:
        raise HTTPException(
            status_code=404, detail="Group with this name does not exist."
        )
    GroupRepository(db).delete_group(group_name=group_data.name)
    return Response(status_code=204, content="Group deleted successfully")
