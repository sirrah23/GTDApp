from src.repo import GTDRepo
from utils import drop_db

DBNAME = "gtd_test"

#TODO: Add Setup and Teardown for tests

def test_store_item():
    drop_db(DBNAME)
    GTDRepo.connect(DBNAME)
    GTDRepo.add_item(description="This is an item", location="inbox")
    assert len(GTDRepo.get_all_items()) == 1
    drop_db(DBNAME)

def test_store_task():
    drop_db(DBNAME)
    GTDRepo.connect(DBNAME)
    GTDRepo.add_task(description="This is a task")
    assert len(GTDRepo.get_all_tasks()) == 1
    drop_db(DBNAME)