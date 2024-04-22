# FastAPI Imports
from fastapi import Depends, HTTPException
from app.models import User
from app.repository_orm.user_orm import users_orm
from app.security.auth_bearer import jwt_bearer

# 3rd Party Imports
import jwt
from decouple import config


async def get_current_user(token: str = Depends(jwt_bearer)) -> User:

    try:
        payload = jwt.decode(
            token, config("JWT_SECRET_KEY"), algorithms=[config("JWT_ALGORITHM")]
        )
    except (jwt.PyJWTError, Exception):
        raise HTTPException(403, {"message": "Could not validate token."})

    user = await users_orm.get_user_by_id(payload["user_id"])
    if not user:
        raise HTTPException(404, {"message": "User does not exist!"})
    return user


async def get_admin_user(
        current_user: User = Depends(get_current_user), ) -> User:
    """
    This function returns an admin user based on the provided token;
    otherwise, raise an authorized exception.
    """

    if not current_user.is_admin:
        raise HTTPException(401, {"message": "Admin priviledge is required!"})

    elif current_user is None:
        return None

    return current_user
