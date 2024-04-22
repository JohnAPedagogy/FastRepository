from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class UserRole(BaseModel):
    id: str
    user_id: str
    role_id: str


class RoleBase(BaseModel):
    role_name: str


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: str
    created: datetime


class Role(RoleBase):
    id: str
    created: datetime
    users: List[UserRole] = []
