import asyncclick as click

from app.db_config.database import db_connect
from app.repository_orm.user_orm import users_orm
from app.security.hashers import pwd_hasher
from app.schemas.user_schemas import UserCreate


@click.command()
@click.option("-e", "--email", type=str, required=True)
@click.option("-pa", "--password", type=str, required=True)
@click.option("-f", "--first_name", type=str, required=True)
@click.option("-l", "--last_name", type=str, required=True)
@click.option("-p", "--phone", type=str, required=True)
@click.option("-ad", "--is_admin", type=str, required=True)
async def create_user(user: UserCreate, is_admin: bool):
    user_data = {
        "email": user.email,
        "password": pwd_hasher.hash_password(user.password),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "is_admin": is_admin,
    }
    await db_connect.connect()
    await users_orm.create_admin(user_data)
    await db_connect.disconnect()


if __name__ == "__main__":
    create_user(_anyio_backend="asyncio")
