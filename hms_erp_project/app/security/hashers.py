# Third Party Imports
from passlib.context import CryptContext


class PasswordHasher:
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.password_context.hash(password)

    def check_password(self, password: str, hashed_password: str) -> bool:
        return self.password_context.verify(password, hashed_password)


pwd_hasher = PasswordHasher()