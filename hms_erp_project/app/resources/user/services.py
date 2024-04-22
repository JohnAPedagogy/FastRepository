from app.repository_orm.user_orm import users_orm
from app.schemas.user_schemas import UserCreate
from app.security.hashers import pwd_hasher
from app.models import User


async def create_user(user: UserCreate) -> User:
    hashed_password = pwd_hasher.hash_password(user.password)
    user = await users_orm.create(user, hashed_password)
    return user


# async def create_admin_user(user: UserCreate) -> User:
#     hashed_password = pwd_hasher.hash_password(user.password)
#     user = await users_orm.create_admin(user, hashed_password)
#     return user
