# import csv
# import os
# from pathlib import Path
# from unittest.mock import patch
# import pytest

# TEST_DATABASE_FILE = "test_tasks.csv"

# TEST_TASKS_CSV = [
#   {
#     "id": "1",
#     "title": "Test Task one",
#     "description": "Test Description One",
#     "status": "Incomplete"
#   },
#   {
#     "id": "2",
#     "title": "Test Task Two",
#     "description": "Test Description Two",
#     "status": "Ongoing"
#   }
# ]

# TEST_TASKS = [
#   {**task, "id": int(task["id"])}
#   for task in TEST_TASKS_CSV
# ]

# @pytest.fixture(autouse=True)
# def create_test_database():
#   database_file_location = str(
#     Path(__file__).parent/TEST_DATABASE_FILE
#   )
#   with patch("operations.DATABASE_FILENAME",
#              database_file_location) as csv_test:
#     with open (database_file_location, mode="w", newline="") as csvfile:
#       writer = csv.DictWriter(
#         csvfile,
#         fieldnames=[
#           "id",
#           "title",
#           "description",
#           "status"
#         ]
#       )

#       writer.writeheader()
#       writer.writerows(TEST_TASKS_CSV)
#     yield csv_test
#     os.remove(database_file_location)

from pathlib import Path
import os
import csv
import pytest
from unittest.mock import patch


TEST_DATABASE = "test_file.csv"

TEST_DATA = [
  {
    "id": "1",
    "title": "Test 1",
    "description": "test 1 desc",
    "status": "ongoing"
  },
  {
    "id": "2",
    "title": "Test 2",
    "description": "test 2 Task desc",
    "status": "ongoing"
  },
  {
    "id": "3",
    "title": "Test 3",
    "description": "test 3 desc",
    "status": "completed"
  },
  {
    "id": "4",
    "title": "Test 4",
    "description": "test 4 desc",
    "status": "completed"
  },
  {
    "id": "5",
    "title": "Test 5",
    "description": "test 5 desc",
    "status": "completed"
  }
]

TEST_TASKS = [{**task, "id":int(task["id"])} for task in TEST_DATA]

@pytest.fixture(autouse=True)
def setup_database():
  test_file_directory = Path(__file__).parent/TEST_DATABASE
  with patch("operations.DATABASE_FILENAME", test_file_directory) as csvtest:
    with open(test_file_directory, mode="w", newline="") as csvfile:
      writer = csv.DictWriter(csvfile, 
                              fieldnames=["id", "title", "description", "status"]
                              )
      writer.writeheader()
      writer.writerows(TEST_DATA)
    yield csvtest
    os.remove(test_file_directory)