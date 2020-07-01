# ATS
Backend for Applicant tracking system using fastapi

---
##Installing the requirements

First step is to make sure you have all the requirements installed. Type this in your terminal:

`pip install -r requirements.txt`

---

##Running the backend

For application startup, run this command and open http://127.0.0.1:8000 on your browser

`uvicorn main:app`

---

@app.put("/jobs/{id}/apply", response_model=schemas.Users)
def update_item(job_id: int,usr_id:int, item: schemas.Users):
  try:
    if item.user_id is usr_id:
      update_item_encoded = jsonable_encoder(item)
      item.job_applied = job_id
      item.job_applied = update_item_encoded

    return {
      "code" : "success",
      "message":"job applied"
    }
  except ValidationError as e:
    print(e)
