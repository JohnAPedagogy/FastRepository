from typing import List
from app.schemas.user_role_schemas import RoleCreate, RoleRead, UserRole
from app.repository_orm.role_orm import role_orm
from app.schemas.responses import ResponseModel
from app.resources.user.router import router
from app.resources.role.utills.rule import RoleChecker
from fastapi import HTTPException
from fastapi import Depends

# Remove dependencies
router.dependencies.clear()


@router.post("/roles/",
             dependencies=[Depends(RoleChecker(["ROLE_ADMIN"]))],
             response_model=RoleRead)
async def create_role(role: RoleCreate):
    new_role = await role_orm.create_role(role=role)
    return ResponseModel(new_role, "Role added successfully.")


@router.post("/users/role",
             dependencies=[Depends(RoleChecker(["ROLE_ADMIN"]))],
             response_model=UserRole)
async def insert_role_to_user(user_id: str, role_id: str):
    user_role = await role_orm.insert_role_to_user(user_id=user_id, role_id=role_id)
    if user_role is None:
        raise HTTPException(status_code=404, detail="Failed to insert role to user")
    return user_role


@router.get("/roles/",
            dependencies=[Depends(RoleChecker(["ROLE_ADMIN"]))],
            response_model=List[RoleRead])
async def read_roles(skip: int = 0, limit: int = 50):
    roles = await role_orm.get_roles(skip=skip, limit=limit)
    return roles


@router.get("/user/{user_id}/roles/",
            dependencies=[Depends(RoleChecker(["ROLE_ADMIN"]))],
            response_model=List[UserRole])
async def read_roles_by_user_id(user_id: str):
    roles = await role_orm.get_roles_by_user_id(user_id=user_id)
    return roles
