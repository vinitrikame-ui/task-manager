from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, SessionLocal

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from database import Base
Base.metadata.create_all(bind=engine)


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)

@app.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)

@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, updated_task: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = crud.update_task(db, task_id, updated_task)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}

@app.patch("/tasks/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.mark_complete(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

    from fastapi import Depends
from sqlalchemy.orm import Session
import models
from auth import hash_password, verify_password, create_access_token

@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    user = models.User(username=username, password=hash_password(password))
    db.add(user)
    db.commit()
    return {"message": "User created"}

@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

                              