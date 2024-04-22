from sqlalchemy.orm import declarative_base
import sqlalchemy as sqlalchemy
import uuid
from sqlalchemy import Boolean, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime

from app.db_config.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    email = Column(String)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    user_roles = relationship("UserRole", back_populates="user")


class Role(Base):
    __tablename__ = "roles"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    role_name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    user_roles = relationship("UserRole", back_populates="role")


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    role_id = Column(String, ForeignKey("roles.id"))
    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")
