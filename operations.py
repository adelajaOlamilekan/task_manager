import csv
from typing import Optional
from models import Task, TaskWithID, TaskV2WithID, TaskV2, UpdateTask
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database.db_config import Tasks
from fastapi import HTTPException, status
# from model

DATABASE_FILENAME = "tasks.csv"
column_fields = ["id", "title", "description", "status"]

def read_all_tasks(db: Session)->list[TaskWithID]:
  # with open(DATABASE_FILENAME) as csvfile:
  #   reader = csv.DictReader(csvfile)
  # return [TaskWithID(**row) for row in reader]
  tasks = db.query(Tasks).all()
  return tasks

def read_task(task_id: int, db: Session)-> Optional[TaskWithID]:
  # with open(DATABASE_FILENAME) as csvfile:
  #   reader = csv.DictReader(csvfile)

  #   for row in reader:
  #     if int(row["id"]) == task_id:
  #       return TaskWithID(**row)
  task = db.query(Tasks).filter(Tasks.id==task_id).first()

def get_next_id()->int:
  try:
    with open(DATABASE_FILENAME) as csvfile:
      reader = csv.DictReader(csvfile)
      return max (int(row["id"]) for row in reader) + 1
  except (FileNotFoundError, ValueError):
    return 1

def write_task_to_csv(task: TaskWithID):
  with open(DATABASE_FILENAME, mode="a", newline="\n") as csvfile:
    writer = csv.DictWriter(
      csvfile, fieldnames=column_fields
    )
    writer.writerow(task.model_dump())

def create_task(task: Task, db:Session) -> TaskWithID:
  # id = get_next_id()
  # task_with_id = TaskWithID(
  #   id = id, 
  #   **task.model_dump()
  # )
  # write_task_to_csv(task_with_id)
  new_task = Tasks(
    title=task.title,
    description=task.description,
    status=task.status
  )

  db.add(new_task)
  db.commit()
  db.refresh(new_task)
  return new_task

def modify_task(task_id: int, task:dict, db:Session)-> Optional[TaskWithID]:
  # updated_task: Optional[TaskWithID] = None
  # tasks = read_all_tasks()

  # for number, task_ in enumerate(tasks):
  #   if task_.id == task_id:
  #     tasks[number] = updated_task = task_.model_copy(update=task)

  # #rewrite the file
  # with open (DATABASE_FILENAME, mode="w", newline="") as csvfile:
  #   writer = csv.DictWriter(csvfile, fieldnames=column_fields)
  #   writer.writeheader()
  #   for task in tasks:
  #     writer.writerow(task.model_dump())
  
  # if updated_task:
  #   return updated_task
  required_task = db.query(Tasks).filter(Tasks.id==task_id).first()

  if not required_task:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Task not found"
    )
  
  for key, value in task.items():
    setattr(required_task, key, value)
  
  db.commit()
  db.refresh(required_task)
  return required_task

def remove_task(task_id:int, db:Session)-> Task:
  # deleted_task: Optional[Task] = None
  # tasks = read_all_tasks()

  # with open(DATABASE_FILENAME, mode="w", newline="") as csvfile:
  #   writer = csv.DictWriter(csvfile, fieldnames=column_fields)
  #   writer.writeheader()
  #   for task in tasks:
  #     if task.id == task_id:
  #       deleted_task = task
  #       continue
  #     writer.writerow(task.model_dump())
    
  #   if deleted_task:
  #     dict_without_id = deleted_task.model_dump()
  #     del dict_without_id["id"]
  #     return Task(**dict_without_id)
  required_task = db.query(Tasks).filter(Tasks.id==task_id).first()
  
  if not required_task:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Task not found"
    )
  
  db.delete(required_task)
  db.commit()
  return required_task

def read_all_tasks_v2()->list[TaskV2WithID]:
  with open(DATABASE_FILENAME) as csvfile:
    reader = csv.DictReader(csvfile)
    return [TaskV2WithID(**row) for row in reader]

def search_for_tasks(keyword:str, db:Session):
  search_term = f"%{keyword}%"
  tasks = db.query(Tasks).filter(
    or_(
      Tasks.title.ilike(search_term),
      Tasks.description.ilike(search_term)
    )
  ).all()

  return tasks