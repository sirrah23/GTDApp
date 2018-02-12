from src.repo import GTDRepo
from utils import drop_db

DBNAME = "gtd_test"

#TODO: Add Setup and Teardown for tests

def test_store_item():
    drop_db(DBNAME)
    GTDRepo.connect(DBNAME)
    GTDRepo.add_item(description="This is an item", location="inbox")
    items = GTDRepo.get_all_items()
    assert len(items) == 1
    assert items[0].description == "This is an item"
    assert items[0].location == "inbox"
    drop_db(DBNAME)

def test_store_task():
    drop_db(DBNAME)
    GTDRepo.connect(DBNAME)
    GTDRepo.add_task(description="This is a task")
    tasks = GTDRepo.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].description == "This is a task"
    assert tasks[0].status == "todo"
    drop_db(DBNAME)

def test_store_project():
    drop_db(DBNAME)
    GTDRepo.add_task(description="Task1")
    GTDRepo.add_task(description="Task2")
    tasks = list(map(lambda t: t.id, GTDRepo.get_all_tasks()))
    GTDRepo.add_project(description="ProjectA",  tasks=tasks)
    projects = GTDRepo.get_all_projects()
    assert len(projects) == 1
    assert projects[0].description == "ProjectA"
    assert len(projects[0].tasks) == 2
    assert projects[0].tasks[0].id in tasks
    assert projects[0].tasks[1].id in tasks
    drop_db(DBNAME)