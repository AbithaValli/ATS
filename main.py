from typing import List
from pydantic import  BaseModel
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
@app.post("/postjobs/",response_model=List[schemas.Jobs])
async def post_jobs(job_name:str,no_of_vacancies:int,job_description:str,admin: schemas.Jobs,db: Session = Depends(get_db)):

  db_user = model.Jobs(job_name=admin.job_name, no_of_vacancies=admin.no_of_vacancies, job_description=admin.job_description)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return {
    "code": "success",
    "message": "job created"
  }

@app.delete("/deletejobs/",response_model=List[schemas.Jobs])
def delete_jobs(id:int,db:Session=Depends(get_db)):
  if model.Users.admin is not 0:
    db_user = db.query(model.Jobs).delete(filter((model.Jobs.job_id)==id))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
  return {
    "code":"success",
    "message":"job deleted"
  }

@app.get("/jobs/{id}", response_model=List[schemas.Jobs])
async def search_jobs(id:int, db:Session=Depends(get_db)):

  records=db.query(model.Jobs.job_id).filter_by(id)
  return {"search result": records}

@app.put("/jobs/{id}/apply", response_model=List[schemas.Jobs])
def apply_job(id:int,db:Session=Depends(get_db)):
  records=db.query(model.Jobs).filter(model.Jobs.job_id == id)
  model.Jobs.no_of_vacancies = model.Jobs.no_of_vacancies-1
  return records
