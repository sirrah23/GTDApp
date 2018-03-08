from GTDApp.repo import GTDRepo
from utils import drop_db, random_objectid
import pytest


@pytest.fixture
def resource():
    GTDRepo.add_user(username="user1", password="mypass", email="user@gtd.com")
    user_id = GTDRepo.get_all_users()[0].id
    yield user_id
    drop_db("gtd_test") #TODO: Read from config?

def test_store_item(resource):
    user_id = resource
    GTDRepo.add_item(description="This is an item", location="inbox", user=user_id)
    items = GTDRepo.get_all_items()
    assert len(items) == 1
    assert items[0]["description"] == "This is an item"
    assert items[0]["location"] == "inbox"

def test_delete_item(resource):
    user_id = resource
    GTDRepo.add_item(description="This is an item", location="inbox", user=user_id)
    items = GTDRepo.get_all_items()
    assert len(items) == 1
    item_id = str(items[0]["id"])
    assert GTDRepo.delete_item(item_id) == True
    items = GTDRepo.get_all_items()
    assert len(items) == 0

def test_delete_two_item(resource):
    user_id = resource
    GTDRepo.add_item(description="This is an item", location="inbox", user=user_id)
    GTDRepo.add_item(description="This is another item", location="inbox", user=user_id)
    items = GTDRepo.get_all_items()
    assert len(items) == 2
    item_id_1 = str(items[0]["id"])
    item_id_2 = str(items[1]["id"])
    assert GTDRepo.delete_item(item_id_1) == True
    assert len(GTDRepo.get_all_items()) == 1
    assert GTDRepo.delete_item(item_id_2) == True
    assert len(GTDRepo.get_all_items()) == 0

def test_delete_nonexistent_item(resource):
    user_id = resource
    assert GTDRepo.delete_item("thisisafakeid") == False

def test_item_to_someday(resource):
    user_id = resource
    item = GTDRepo.add_item(description="This is an item", location="inbox", user=user_id)
    someday_item = GTDRepo.item_to_someday(item["id"], user_id)
    assert someday_item is not None
    assert item["id"] == someday_item["id"]
    assert item["description"] == someday_item["description"]
    assert someday_item["location"] == "someday/maybe"

def test_item_to_task(resource):
    user_id = resource
    GTDRepo.add_item(description="Thing", location="inbox", user=user_id)
    added_item = GTDRepo.get_all_items()[0]
    task = GTDRepo.item_to_task(added_item["id"], user_id)
    # No more items
    assert len(GTDRepo.get_all_items()) == 0
    # Task used to be the item
    assert task is not None
    assert task["description"] == "Thing"

def test_item_to_project(resource):
    user_id = resource
    item = GTDRepo.add_item(description="Thing", location="inbox", user=user_id)
    project = GTDRepo.item_to_project(item["id"], user_id)
    assert project is not None
    assert len(GTDRepo.get_all_items()) == 0
    assert project["description"] == "Thing"

def test_store_task(resource):
    user_id = resource
    GTDRepo.add_task(description="This is a task", user=user_id)
    tasks = GTDRepo.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]["description"] == "This is a task"
    assert tasks[0]["status"] == "todo"

def test_toggle_task_todo_to_done(resource):
    user_id = resource
    GTDRepo.add_task(description="This is a task", user=user_id)
    tasks = GTDRepo.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]["description"] == "This is a task"
    assert tasks[0]["status"] == "todo"
    assert GTDRepo.toggle_task(str(tasks[0]["id"])) == True
    tasks = GTDRepo.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]["description"] == "This is a task"
    assert tasks[0]["status"] == "done"

def test_toggle_task_done_to_todo(resource):
    user_id = resource
    GTDRepo.add_task(description="This is a task", user=user_id, status="done")
    tasks = GTDRepo.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]["description"] == "This is a task"
    assert tasks[0]["status"] == "done"
    assert GTDRepo.toggle_task(str(tasks[0]["id"])) == True
    tasks = GTDRepo.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]["description"] == "This is a task"
    assert tasks[0]["status"] == "todo"

def test_task_to_project(resource):
    user_id = resource
    task = GTDRepo.add_task(description="Thing", user=user_id)
    project = GTDRepo.task_to_project(task["id"], user_id)
    # No more tasks
    assert len(GTDRepo.get_all_tasks()) == 0
    # Project used to be the task
    assert project is not None
    assert project["description"] == "Thing"

def test_delete_task(resource):
    user_id = resource
    task_to_del = GTDRepo.add_task(description="This is a task", user=user_id)
    GTDRepo.add_task(description="This is another task", user=user_id)
    assert len(GTDRepo.get_all_tasks()) == 2
    assert GTDRepo.delete_task(task_to_del["id"], user_id) == True
    remaining_tasks = GTDRepo.get_all_tasks()
    assert len(remaining_tasks) == 1
    assert remaining_tasks[0]["description"] == "This is another task"

def test_store_project(resource):
    user_id = resource
    GTDRepo.add_task(description="Task1", user=user_id)
    GTDRepo.add_task(description="Task2", user=user_id)
    tasks = list(map(lambda t: t["id"], GTDRepo.get_all_tasks()))
    GTDRepo.add_project(description="ProjectA",  tasks=tasks, user=user_id)
    projects = GTDRepo.get_all_projects()
    assert len(projects) == 1
    assert projects[0]["description"] == "ProjectA"
    assert len(projects[0]["tasks"]) == 2
    assert projects[0]["tasks"][0]["id"] in tasks
    assert projects[0]["tasks"][1]["id"] in tasks

def test_store_project_task(resource):
    user_id = resource
    added_proj_one = GTDRepo.add_project(description="ProjectA", user=user_id, tasks=[])
    assert len(added_proj_one["tasks"]) == 0
    added_subtask = GTDRepo.add_project_task(added_proj_one["id"], "ProjectASubtask", user_id)
    added_proj_two = GTDRepo.get_all_projects()[0]
    assert len(added_proj_two["tasks"]) == 1
    assert added_proj_one["id"] == added_proj_two["id"]
    assert added_subtask["id"] in map(lambda t: t["id"], added_proj_two["tasks"])

def test_delete_project_task_good(resource):
    """
    Successfully delete a subtask for a given project.
    """
    user_id = resource
    proj = GTDRepo.add_project(description="ProjectA", user=user_id, tasks=[])
    subtask = GTDRepo.add_project_task(proj["id"], "ProjectASubtask", user_id)
    assert GTDRepo.delete_project_task(proj["id"], subtask["id"], user_id) == True
    proj = GTDRepo.get_all_projects()[0]
    assert len(proj["tasks"]) == 0

def test_delete_project_task_bad(resource):
    """
    Should not be able to delete a task if it does not belong to the project
    """
    user_id = resource
    proj = GTDRepo.add_project(description="ProjectA", user=user_id, tasks=[])
    task = GTDRepo.add_task(description="Task1", user=user_id)
    assert GTDRepo.delete_project_task(proj["id"], task["id"], user_id) == False
