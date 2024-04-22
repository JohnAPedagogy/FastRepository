# Stdlib Imports
from datetime import datetime, timedelta
from typing import Dict, Any, Union

# FastAPI Imports
from fastapi import HTTPException

# PyJWT Imports
import jwt

# Third Party Imports
from app.core.settings import hms_settings


# JWT Env Definitions
JWT_SECRET = hms_settings.JWT_SECRET_KEY
JWT_ALGORITHM = hms_settings.JWT_ALGORITHM
TOKEN_LIFETIME = hms_settings.TOKEN_LIFETIME


class AuthHandler:
    def __init__(
        self,
        secret: str = JWT_SECRET,
        algorithm: str = JWT_ALGORITHM,
        token_lifetime: int = TOKEN_LIFETIME,
    ):
        self.JWT_SECRET = secret
        self.JWT_ALGORITHM = algorithm
        self.TOKEN_LIFETIME = token_lifetime

    def sign_jwt(self, user_id: int) -> Dict[str, Any]:
        payload = {
            "user_id": user_id,
            "expires": str(
                datetime.now() + timedelta(minutes=self.TOKEN_LIFETIME)
            ),
        }
        token = jwt.encode(
            payload, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM
        )
        return {"access_token": token}

    def decode_jwt(self, token: str) -> Union[Dict, Exception]:
        try:
            decoded_token = jwt.decode(
                token, self.JWT_SECRET, algorithms=self.JWT_ALGORITHM
            )
        except (jwt.DecodeError, Exception):
            raise HTTPException(403, {"message": "Token invalid."})

        if (
            datetime.strptime(decoded_token["expires"], "%Y-%m-%d %H:%M:%S.%f")
            >= datetime.now()
        ):
            return decoded_token
        raise HTTPException(400, {"message": "Token expired."})


authentication = AuthHandler()
