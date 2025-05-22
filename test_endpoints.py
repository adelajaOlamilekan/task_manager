from conftest import (
  TEST_DATA,
  TEST_TASKS
)
from main import app
from fastapi.testclient import TestClient
from operations import read_all_tasks, read_task

client = TestClient(app)

def test_read_all_tasks():
  response = client.get("/tasks")
  assert response.status_code == 200
  assert response.json() == TEST_TASKS

def test_read_a_task():
  response = client.get("/task/1")
  assert response.status_code == 200
  assert response.json() == TEST_TASKS[0]
  response = client.get("/task/7")
  assert response.status_code == 404

def test_add_task():
  task = {
    "title": "a newly added task",
    "description": "this is a newly added task",
    "status": "completed"
  }
  response = client.post("/task", json=task)
  assert response.status_code == 200
  assert response.json() == {**task, "id": 6}
  assert len(read_all_tasks()) == 6


def test_update_task():
  updated_fields = {"status": "completed"}
  response = client.put("/task/2", json=updated_fields)
  
  assert response.status_code == 200
  assert response.json() == {
    **TEST_TASKS[1],
    **updated_fields
  }

  response = client.put("/task/8", json=updated_fields)
  assert response.status_code == 404

def test_delete_task():
  response = client.delete("/task/2")
  assert response.status_code == 200
  expected_response = TEST_TASKS[1]
  del expected_response["id"]

  assert response.json() == expected_response
  assert read_task(2) is None

  response = client.delete("task/9")
  assert response.status_code == 404

def test_search_task():
  keyword = "task"

  response = client.get(f"/tasks/search?keyword={keyword}")

  assert response.status_code == 200
  assert len(response.json())== 1
  TEST_TASKS[1].update({"id": 2})
  assert response.json()[0] == TEST_TASKS[1]

  keyword = "kangaroo"
  response = client.get(f"/tasks/search/{keyword}")
  assert response.status_code == 404