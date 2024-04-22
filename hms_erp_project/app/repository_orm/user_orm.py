from sqlalchemy.orm import joinedload
from app.models import User
from app.schemas.user_schemas import UserCreate, UserList
from app.repository_orm.irepository import IRepository, SurrealORM, PostGresORM
from pydantic import EmailStr
from decouple import config


class BaseUsersORM(IRepository):#postgres orm
    def partial_list(self):
        return self.orm.query(User)


class UserRepository(BaseUsersORM):
    async def get_user_by_id(self, user_id: int) -> User:
        """This method gets a user from the database."""
        user = (
            self.partial_list()
            .options(joinedload(User.user_roles))
            .filter(User.id == user_id)
            .first()
        )
        return user

    async def get_user_by_email(self, user_email: EmailStr) -> User:
        user = (
            self.partial_list()
            .options(joinedload(User.user_roles))
            .filter(User.email == user_email)
            .first()
        )
        return user

    def list(self) -> UserList:
        """This method gets all the users from the database."""
        return [user_data.dict() for user_data in self.orm.query(User).all()]

    async def create(self, user_data: UserCreate, password: str) -> User:
        """This method creates a new user."""
        user = User(email=user_data.email,
                    first_name=user_data.first_name,
                    last_name=user_data.last_name,
                    phone=user_data.phone,
                    password=password)
        self.orm.add(user)
        self.orm.commit()
        self.orm.refresh(user)

        return user

    async def create_admin(self, user_data: UserCreate, is_admin: bool) -> User:
        """This method creates an admin user."""
        admin_user = User(email=user_data.email,
                          first_name=user_data.first_name,
                          last_name=user_data.last_name,
                          phone=user_data.phone,
                          password=user_data.password,
                          is_admin=is_admin)
        self.orm.add(admin_user)
        self.orm.commit()
        self.orm.refresh(admin_user)

        return admin_user

ORM_SETTING = config('ORM_SETTING')
if(ORM_SETTING == "POSTGRES"):
    users_orm = UserRepository(PostGresORM)
# elif(ORM_SETTING == "MONGO_DB"):
#     users_orm = UserRepository(MongORM)
elif(ORM_SETTING == "SURREAL"):
    users_orm = UserRepository(SurrealORM)
