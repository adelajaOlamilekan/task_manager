from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from models import (
  Task,
  TaskWithID,
  UpdateTask,
  TaskV2WithID,
  UserInDB,
  User
)
from operations import (
  read_all_tasks,
  read_task,
  create_task,
  modify_task,
  remove_task,
  read_all_tasks_v2,
  search_for_tasks
)
from typing import Optional
from database.db_config import get_db
from dependency import get_api_version
from fastapi.security import OAuth2PasswordRequestForm
from security import(
  fake_token_generator,
  fakely_hashed_password,
  fake_users_db,
  get_user_from_token
)
from fastapi.openapi.utils import get_openapi

def custom_openapi():
  if app.openapi_schema:
    return app.openapi_schema
  openapi_schema = get_openapi(
    title="Customized Title",
    version="2.0.0",
    description="Custom OpenAPI Schema",
    routes=app.routes
  )
  del openapi_schema["paths"]["/token"]
  app.openapi_schema = openapi_schema
  return app.openapi_schema

app = FastAPI(title="Task Manager API",
              description="This is a task management API",
              version="0.1.0")

app.openapi = custom_openapi

@app.get("/tasks", response_model=list[TaskWithID])
def get_tasks(task_status: Optional[str]=None, 
              title:Optional[str]=None, 
              db: Session = Depends(get_db)):
  tasks = read_all_tasks(db)

  # if task_status:
  #   tasks =[
  #     task 
  #     for task in tasks
  #     if task.status == task_status
  #   ]
  
  # if title:
  #   tasks = [
  #     task
  #     for task in tasks
  #     if task.title == title
  #   ]

  # if not tasks:
  #   raise HTTPException(
  #     status_code=status.HTTP_404_NOT_FOUND,
  #     detail= "No task found"
  #   )
  
  return tasks

@app.get("/task/{task_id}", response_model=TaskWithID)
def get_task(task_id:int, 
             db:Session = Depends(get_db)):
  task = read_task(task_id, db)

  if not task:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail= "Task not found"
    )
  
  return task

@app.post("/task", response_model=TaskWithID)
def add_task(task: Task, 
             db:Session= Depends(get_db)):
  return create_task(task, db)

@app.put("/task/{task_id}", response_model=TaskWithID)
def update_task(task_id: int, 
                task: UpdateTask,
                db:Session = Depends(get_db)):
  modified_task = modify_task(task_id, 
                              task.model_dump(exclude_unset=True),
                              db)
  if not modified_task:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Task not found"
    )
  return modified_task

@app.delete("/task/{task_id}", response_model=Task)
def delete_task(task_id:int,
                db:Session=Depends(get_db)):
  removed_task = remove_task(task_id, db)

  if not removed_task:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Task not found"
    )
  
  return removed_task

@app.get("/tasks/search", response_model=list[TaskWithID])
def search_tasks(keyword: str, db:Session=Depends(get_db)):
  # tasks = read_all_tasks()
  # filtered_tasks = [
  #   task for task in tasks
  #   if keyword.lower() in (task.title + task.description).lower()
  # ]

  # if not filtered_tasks:
  #   raise HTTPException(
  #     status_code= status.HTTP_404_NOT_FOUND,
  #     detail="No task found"
  #   )
  filtered_tasks = search_for_tasks(keyword, db)
  if not filtered_tasks:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Tasks not found"
    )
  
  return filtered_tasks

@app.get("/tasks/", response_model=list[TaskV2WithID])
def get_tasks_v2(x_api_version:int=Depends(get_api_version),
                 db:Session=Depends(get_db)):
  # print("Version 2")
  if x_api_version == 1:
    tasks = read_all_tasks(db)
  elif x_api_version == 2:
    tasks = read_all_tasks_v2()

  return tasks

@app.post("/token")
async def login(
  form_data: OAuth2PasswordRequestForm = Depends()
):
  user_dict = fake_users_db.get(form_data.username)
  if not user_dict:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="incorrect username or password"
    )
  user = UserInDB(**user_dict)
  hashed_password = fakely_hashed_password(
    form_data.password
  )

  if not hashed_password == user.hashed_password:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Incorrect username or password"
    )
  
  token = fake_token_generator(user)
  return {
    "access_token": token,
    "token_type": "bearer"
  }

@app.get("/users/me", response_model=User)
def read_users_me(
  current_user: User = Depends(get_user_from_token)
):
  return current_user