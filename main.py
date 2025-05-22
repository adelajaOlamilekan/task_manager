from fastapi import FastAPI, HTTPException, status
from models import (
  Task,
  TaskWithID,
  UpdateTask,
  TaskV2WithID
)
from operations import (
  read_all_tasks,
  read_task,
  create_task,
  modify_task,
  remove_task,
  read_all_tasks_v2
)
from typing import Optional

app = FastAPI()

@app.get("/tasks", response_model=list[TaskWithID])
def get_tasks(task_status: Optional[str]=None, title:Optional[str]=None):
  tasks = read_all_tasks()

  if task_status:
    tasks =[
      task 
      for task in tasks
      if task.status == task_status
    ]
  
  if title:
    tasks = [
      task
      for task in tasks
      if task.title == title
    ]

  if not tasks:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail= "No task found"
    )
  
  return tasks

@app.get("/task/{task_id}", response_model=TaskWithID)
def get_task(task_id:int):
  task = read_task(task_id)

  if not task:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail= "Task not found"
    )
  
  return task

@app.post("/task", response_model=TaskWithID)
def add_task(task: Task):
  return create_task(task)

@app.put("/task/{task_id}", response_model=TaskWithID)
def update_task(task_id: int, task: UpdateTask):
  modified_task = modify_task(task_id, task.model_dump(exclude_unset=True))
  if not modified_task:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Task not found"
    )
  return modified_task

@app.delete("/task/{task_id}", response_model=Task)
def delete_task(task_id:int):
  removed_task = remove_task(task_id)

  if not removed_task:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Task not found"
    )
  
  return removed_task

@app.get("/tasks/search", response_model=list[TaskWithID])
def search_tasks(keyword: str):
  tasks = read_all_tasks()
  filtered_tasks = [
    task for task in tasks
    if keyword.lower() in (task.title + task.description).lower()
  ]

  if not filtered_tasks:
    raise HTTPException(
      status_code= status.HTTP_404_NOT_FOUND,
      detail="No task found"
    )

  return filtered_tasks

@app.get("/v2/tasks", response_model=list[TaskV2WithID])
def get_tasks_v2():
  tasks = read_all_tasks_v2()
  return tasks