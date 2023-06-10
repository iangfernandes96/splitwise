#!/usr/bin/python3

from sqlalchemy.orm import Session
from models import Group, User
from typing import Optional
from common import MemberValidationError
from schemas.group import GroupCreateSchema
from repositories import UserRepository


class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_group_by_id(self, id: str) -> Optional[Group]:
        return self.db.query(Group).filter(Group.id == id).first()

    def get_group_by_name(self, name: str) -> Optional[Group]:
        return self.db.query(Group).filter(Group.name == name).first()

    def create_group(self, group_data: GroupCreateSchema, current_user: User):
        group_members = group_data.group_members

        # Validate if group members are on splitwise
        if not UserRepository(self.db).validate_members(
            group_members=group_members
        ):  # noqa
            raise MemberValidationError

        group = Group(
            name=group_data.name,
            members=group_data.group_members,
            owner_email=current_user.email,
            owner=current_user,  # noqa
        )
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        return group

    def delete_group(self, group_name: str):
        group = self.db.query(Group).filter(Group.name == group_name).first()
        self.db.delete(group)
        self.db.commit()
        return None
