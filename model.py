from sqlalchemy import Column, Integer, String, Boolean,DDL,event
from database import Base



class Users(Base):
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)


    job_applied = Column(String(45))
    user_name = Column(String(45))
event.listen(
    Users.__table__,
    "after_create",
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 501;")
)
class Jobs(Base):
  __tablename__ = "Jobs"

  job_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  job_name = Column(String(25), index=True)
  no_of_vacancies = Column(Integer, index=True)
  job_description = Column(String(255))

class Recruiter(Base):
  __tablename__ = "Recruiter"

  adm_id = Column(Integer,primary_key=True,index=True,autoincrement=True)
  adm_name = Column(String(25),index=True)
  job_posted = Column(Integer,index=True)
