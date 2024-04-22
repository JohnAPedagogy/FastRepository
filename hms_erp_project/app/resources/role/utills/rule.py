from typing import List
from fastapi import Depends, HTTPException
from app.schemas.user_schemas import User
from app.core.deps import get_current_user
from app.repository_orm.role_orm import role_orm


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        user_roles = role_orm.get_roles_by_email(user.email)
        roles = role_orm.get_role_names(user_roles)
        for role in roles:
            if role not in self.allowed_roles:
                raise HTTPException(status_code=403, detail="Operation not permitted")