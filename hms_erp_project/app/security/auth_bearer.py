# FastAPI Imports
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Own Imports
from app.security.auth_handler import authentication


class JWTBearer(HTTPBearer):
    """Responsible for persisting authentication on our API routes."""

    def __init__(self, auto_error: bool = True):

        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        authorization_credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)

        if authorization_credentials:
            if authorization_credentials.scheme != "Bearer":
                raise HTTPException(403, {"message": "Invalid authentication scheme."})

            if not self.verify_jwt_token(authorization_credentials.credentials):
                raise HTTPException(403, {"message": "Invalid token or expired token."})

            return authorization_credentials.credentials
        else:
            raise HTTPException(403, {"message": "Invalid authorization code."})

    def verify_jwt_token(self, token: str) -> bool:
        payload = authentication.decode_jwt(token)

        if payload:
            return True
        return False


jwt_bearer = JWTBearer()
