from typing import Optional, List, Union
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.schemas.user_role_schemas import UserRole


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class User(UserBase):
    id: str
    is_active: bool
    is_admin: bool
    created: datetime
    roles: List[UserRole] = []


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class UserConfirmation(BaseModel):
    user_id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone: str


class UserList(BaseModel):
    users: List[UserConfirmation]


class UserRegisterResponse(BaseModel):
    id: int


class userConfirmation(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str






