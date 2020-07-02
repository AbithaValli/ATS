from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Users(Base):
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    admin = Column(Boolean)
    job_applied = Column(String(45))
    user_name = Column(String(45))

class Jobs(Base):
  __tablename__ = "Jobs"

  job_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  job_name = Column(String(25), index=True)
  no_of_vacancies = Column(Integer, index=True)
  job_description = Column(String(255))
