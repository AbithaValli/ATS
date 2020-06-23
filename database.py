import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import mysql.connector
# default
#engine = create_engine('mysql://root:panda99@localhost/ats')


user_name = "root"
password = "panda99"
host = "localhost"
database_name = "ats"

db = 'mysql+mysqlconnector://%s:%s@%s/%s?charset=utf8' % (
    user_name,
    password,
    host,
    database_name,
)


engine = create_engine(
    db,
    encoding="utf-8",
    echo=True,
)


SessionLocal = scoped_session(

    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)
Base = declarative_base()

Base.query = SessionLocal.query_property()
