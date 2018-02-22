from src.repo import GTDRepo
from utils import drop_db, random_objectid
import pytest

DBNAME = "gtd_test"

GTDRepo.connect(DBNAME)

@pytest.fixture
def resource():
    GTDRepo.add_user(username="user1", password="mypass", email="user@gtd.com")
    user_id = GTDRepo.get_all_users()[0].id
    yield user_id
    drop_db(DBNAME)

def test_store_item(resource):
    user_id = resource
    GTDRepo.add_item(description="This is an item", location="inbox", user=user_id)
    items = GTDRepo.get_all_items()
    assert len(items) == 1
    assert items[0].description == "This is an item"
    assert items[0].location == "inbox"
    assert items[0].user.id == user_id

def test_store_task(resource):
    user_id = resource
    GTDRepo.add_task(description="This is a task", user=user_id)
    tasks = GTDRepo.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].description == "This is a task"
    assert tasks[0].status == "todo"
    assert tasks[0].user.id == user_id

def test_store_project(resource):
    user_id = resource
    GTDRepo.add_task(description="Task1", user=user_id)
    GTDRepo.add_task(description="Task2", user=user_id)
    tasks = list(map(lambda t: t.id, GTDRepo.get_all_tasks()))
    GTDRepo.add_project(description="ProjectA",  tasks=tasks, user=user_id)
    projects = GTDRepo.get_all_projects()
    assert len(projects) == 1
    assert projects[0].description == "ProjectA"
    assert len(projects[0].tasks) == 2
    assert projects[0].tasks[0].id in tasks
    assert projects[0].tasks[1].id in tasks
    assert projects[0].user.id == user_id
