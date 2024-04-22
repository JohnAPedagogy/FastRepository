from sqlalchemy.orm import joinedload
from app.models import Role, UserRole, User
from app.schemas.user_schemas import UserCreate, UserList
from app.schemas.user_role_schemas import RoleCreate
from app.repository_orm.irepository import IRepository
from pydantic import EmailStr
from typing import List


class BaseRolesORM(IRepository):
    def partial_list(self):
        return self.orm.query(Role)


class RoleRepository(BaseRolesORM):
    async def create_role(self, role: RoleCreate) -> Role:
        user_role = Role(role_name=role.role_name)
        self.orm.add(user_role)
        self.orm.commit()
        self.orm.refresh(user_role)
        return user_role

    async def insert_role_to_user(self, role_id: str, user_id: str):
        user_role = UserRole(role_id=role_id, user_id=user_id)
        self.orm.add(user_role)
        self.orm.commit()
        self.orm.refresh(user_role)
        return user_role

    async def remove_role_to_user(self, role_id: str, user_id: str):
        db_user_role = UserRole(role_id=role_id, user_id=user_id)
        self.orm.delete(db_user_role)
        self.orm.commit()
        self.orm.refresh(db_user_role)
        return db_user_role

    async def get_roles_by_user_id(self, user_id: str):
        user = (
            self.partial_list()
            .filter(User.id == user_id)
            .first()
        )
        return user.user_roles

    async def get_roles_by_email(self, user_email: EmailStr) -> User:
        user = (
            self.partial_list()
            .filter(User.email == user_email)
            .first()
        )
        return user.user_roles

    async def get_roles(self, roles: List[UserRole]) -> UserList:
        """This method gets all the users from the database."""
        return [user_role.dict() for user_role in self.orm.query(Role).all()]

    def get_role_names(self, roles: List[UserRole]):
        names = list()
        for role in roles:
            role_item = self.orm.query(Role).filter(Role.id == role.id).first()
            names.append(role_item.role_name)
        return names


role_orm = RoleRepository()
