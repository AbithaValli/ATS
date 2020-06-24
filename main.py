from typing import List
from pydantic import  BaseModel,ValidationError
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from sqlalchemy import table,column
import model, schemas
from database import SessionLocal, engine

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



@app.get("/users/", response_model=List[schemas.Users])
def show_users(db: Session = Depends(get_db)):
    records = db.query(model.Users).all()
    return records

@app.get("/jobs/", response_model=List[schemas.Jobs])
def show_jobs(db: Session = Depends(get_db)):

    records = db.query(model.Jobs).all()
    return records
@app.post("/postjobs/",response_model=schemas.Jobs)
def post_jobs(j_name,vacancies,j_desc,admin:schemas.Jobs,db: Session = Depends(get_db)):

  db_user = model.Jobs(job_name=j_name, no_of_vacancies=vacancies, job_description=j_desc)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

@app.delete("/deletejobs/",response_model=schemas.Jobs)
def delete_jobs(id:int,db:Session=Depends(get_db)):
  if model.Users.admin is not 0:
    db_user = model.Jobs(job_id=id)
    db.delete(db_user)
    db.commit()
    db.refresh(db_user)
  return {
    "code":"success",
    "message":"job deleted"
  }

@app.get("/jobs/{id}", response_model=schemas.Jobs)
def search_jobs(id:int, db:Session=Depends(get_db)):
  try:
    records = db.query(model.Jobs).filter(model.Jobs.job_id == id).first()
    return records
  except ValidationError as e:
    print(e)



@app.put("/jobs/{id}/apply", response_model=List[schemas.Jobs])
def apply_job(id:int,db:Session=Depends(get_db)):
  records=db.query(model.Jobs).filter(model.Jobs.job_id == id)
  model.Jobs.no_of_vacancies = model.Jobs.no_of_vacancies-1
  return records
