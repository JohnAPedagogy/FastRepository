from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from decouple import config

# Third Party Imports
from databases import Database

SQLALCHEMY_DATABASE_URL = f"{config('DB_NAME')}://{config('DB_USER')}:" \
                              f"{config('DB_PASSWORD')}@{config('DB_SERVER')}:" \
                              f"{config('DB_PORT')}/{config('DB_NAME_DATABASE')}"

DB_ENGINE = create_engine(SQLALCHEMY_DATABASE_URL)

# Construct a session maker
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=DB_ENGINE)
SessionLocal = scoped_session(session_factory)
Base = declarative_base()
db_connect = Database(SQLALCHEMY_DATABASE_URL)



