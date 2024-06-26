# FastAPI Imports
from fastapi import Depends, HTTPException

# Own Imports
from app.schemas.user_schemas import User
from app.resources.user.router import router
from app.repository_orm.user_orm import users_orm
from app.core.deps import get_current_user, get_admin_user


@router.get("/users/", response_model=list[User])
async def users_info(
    skip: int = 0, limit: int = 100, admin_user: User = Depends(get_admin_user)
):

    if admin_user is None:
        raise HTTPException(404, {"message": "Admin user does not exist!"})

    users = await users_orm.list(skip, limit)
    return users


@router.get("/users/me/", response_model=User)
async def user_info(current_user: User = Depends(get_current_user)):

    user = await users_orm.get(user_id=current_user.id)
    return user
