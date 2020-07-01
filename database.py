import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# default
engine = create_engine('mysql://root:panda99@localhost/ats')
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="panda99",
  database="ats"
)

dbcursor = db.cursor()


#db = mysql.connector.connect(
 # host="localhost",
  #user="root",
  #password="panda99",
  #database="ats"
#)




SessionLocal = scoped_session(

    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)
Base = declarative_base()

Base.query = SessionLocal.query_property


