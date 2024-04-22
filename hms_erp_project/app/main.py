from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.resources.user.auth import router as auth_router
from app.resources.user.api import router as users_router
from app.resources.role.user_role import router as roles_router


from app.db_config.database import db_connect


origins = [
    "http://localhost"
]

app = FastAPI()
app.include_router(auth_router)
app.include_router(users_router, tags=["Users"])
app.include_router(roles_router, tags=["Roles"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await db_connect.connect()


@app.on_event("shutdown")
async def shutdown():
    await db_connect.disconnect()




