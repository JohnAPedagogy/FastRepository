# FastAPI Imports
from fastapi import APIRouter, Depends

# Own Imports
from app.security.auth_bearer import jwt_bearer


# initialize router
router = APIRouter(dependencies=[Depends(jwt_bearer)])
