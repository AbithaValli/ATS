from pydantic import BaseModel
from typing import Optional


class Users(BaseModel):
    user_id: Optional[int]
    admin: Optional[bool]
    job_applied: Optional[str]

    class Config:
        orm_mode = True


class Jobs(BaseModel):
  job_id: int
  job_name: str
  no_of_vacancies: int
  job_description: str

  class Config:
    orm_mode = True



