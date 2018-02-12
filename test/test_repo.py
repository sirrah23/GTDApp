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