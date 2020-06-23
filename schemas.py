from pydantic import BaseModel



class Users(BaseModel):
    user_id: int
    admin: bool
    job_applied: str

    class Config:
        orm_mode = True


class Jobs(BaseModel):

  job_name: str
  no_of_vacancies: int
  job_description: str

  class Config:
    orm_mode = True
