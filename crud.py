from sqlalchemy.orm import Session
import models, schemas

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session):
    return db.query(models.Task).all()

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def update_task(db: Session, task_id: int, updated_task: schemas.TaskCreate):
    task = get_task(db, task_id)
    if task:
        task.title = updated_task.title
        task.description = updated_task.description
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)
    if task:
        db.delete(task)
        db.commit()
    return task

def mark_complete(db: Session, task_id: int):
    task = get_task(db, task_id)
    if task:
        task.completed = True
        db.commit()
        db.refresh(task)
    return task