from conftest import TEST_TASKS_CSV
from models import Task, TaskWithID
from operations import(
  create_task,
  get_next_id,
  modify_task,
  read_all_tasks,
  read_task,
  remove_task,
  write_task_to_csv
)

def test_read_all_task():
  assert read_all_tasks() == [TaskWithID(**task) for task in TEST_TASKS_CSV]

def test_get_next_id():
  assert get_next_id() == 3

def test_write_task_to_csv():
  test_task = TaskWithID(
    id=3,
    title="Test Task 3",
    description="Test Task Description 3",
    status="Ongoing"
  )

  write_task_to_csv(test_task)

  assert read_all_tasks() == list(
    map(lambda task: TaskWithID(**task), TEST_TASKS_CSV)
  ) + [test_task]

def test_create_task():
  task = Task(
    title="Test Task",
    description="Test Task Description",
    status="Completed"
  )

  task_with_id = TaskWithID(
    id=3,
    **task.model_dump()
  )
  result = create_task(task) 
  
  assert result.id == 3
  
  assert read_task(3) == TaskWithID(id=3, **task.model_dump())

def test_read_task():
  assert read_task(1) == TaskWithID(**TEST_TASKS_CSV[0])

def test_modify_task():
  update_task = {
    "title": "test 2 title is now changed"
  }

  assert modify_task(2, update_task) == read_task(2)
  assert modify_task(2, update_task).title == "test 2 title is now changed"

def test_remove_task():
  #remove a none existing task
  assert remove_task(3) is None 

  #remove an existing task
  remove_task(1)

  assert read_task(1) is None