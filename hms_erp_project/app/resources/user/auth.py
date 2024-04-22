# FastAPI Imports
from fastapi import HTTPException

# Own Imports
from app.resources.user.router import router
from app.resources.user.services import create_user
from app.security.auth_bearer import authentication
from app.security.hashers import pwd_hasher
from app.schemas.auth_schemas import UserLoginSchema
from app.repository_orm.user_orm import users_orm
from app.schemas.user_schemas import UserCreate, User
from app.schemas.responses import ResponseModel, ErrorResponseModel

# Remove dependencies
router.dependencies.clear()


@router.post("/register/", response_model=User)
async def create_new_user(user_data: UserCreate):
    user = await users_orm.get_user_by_email(user_data.email)

    if user:
        return ErrorResponseModel("An error occurred.", 404, "User already exists!")
    new_user = await create_user(user_data)
    return ResponseModel(new_user, "User added successfully.")


@router.post("/login/")
async def login_user(authenticate: UserLoginSchema):
    user = await users_orm.get_email(authenticate.email)

    if user:
        user_token = authentication.sign_jwt(user.id)

        if pwd_hasher.check_password(authenticate.password, user.password):
            return user_token

        raise HTTPException(401, {"message": "Password incorrect!"})
    raise HTTPException(404, {"message": "User does not exist!"})
