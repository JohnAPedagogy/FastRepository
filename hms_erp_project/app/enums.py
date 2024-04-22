from enum import Enum


class HSMEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


class RoleType(HSMEnum):
    user = "user"
    staff = "staff"
    admin = "admin"
    doctor = "doctor"


class UserState(HSMEnum):
    enable = "enable"
    disable = "disable"
