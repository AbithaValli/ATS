from typing import List
from pydantic import  BaseModel,ValidationError
from fastapi import Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from sqlalchemy import table,column
import model, schemas
from database import SessionLocal,engine, dbcursor

model.Base.metadata.create_all(bind=engine)

app = FastAPI()




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


#displays all the users
@app.get("/users/", response_model=List[schemas.Users])
def show_users(db: Session = Depends(get_db)):
    records = db.query(model.Users).all()
    return records
#displays all the jobs
@app.get("/jobs/", response_model=List[schemas.Jobs])
def show_jobs(db: Session = Depends(get_db)):

    records = db.query(model.Jobs).all()
    return records
#adding new jobs to the jobs table
@app.post("/postjobs/",response_model=schemas.Jobs)
def post_jobs(j_name,vacancies,j_desc,db: Session = Depends(get_db)):

  db_user = model.Jobs(job_name=j_name, no_of_vacancies=vacancies, job_description=j_desc)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user
#deleting selected jobfrom ats.jobs
@app.delete("/deletejobs/")
def delete_jobs(id:int,db:Session=Depends(get_db)):
  try:

    records = db.query(model.Jobs).filter(model.Jobs.job_id == id).first()
    db.delete(records)
    db.commit()
    #db.refresh(records)

    return{
    "code":"success"
    }
  except ValidationError as e:
    print(e)

  #@app.delete("/user/{job_id}", response_model=schemas.Jobs, responses={404: {"model": HTTPNotFoundError}})
  #async def delete_user(id: int):
  #  deleted_count = await model.Jobs.filter(job_id=id).delete()
   # if not deleted_count:
    #  raise HTTPException(status_code=404, detail=f"User {id} not found")
    #return Status(message=f"Deleted user {id}")


#fwtching the job details from ats.jobs based on the job_id
@app.get("/jobs/{id}", response_model=schemas.Jobs)
def search_jobs(id:int, db:Session=Depends(get_db)):
  try:
    records = db.query(model.Jobs).filter(model.Jobs.job_id == id).first()
    return records
  except ValidationError as e:
    print(e)
#updates the users table for the jobs applied by the users


@app.put("/jobs/{id}/apply",response_model=schemas.Users)
def apply_job(JobName,userid,db:Session=Depends((get_db))):
    try:
      records = db.query(model.Users).filter(model.Users.user_id == userid).first()
      #db_user=records(job_applied = JobName)
      db.__setattr__(records.job_applied,JobName)
      db.commit()
      db.refresh(records)

      return {
      "code":"successful"
    }

    except ValidationError as e:
      print(e)

