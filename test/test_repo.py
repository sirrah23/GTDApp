from src.repo import GTDRepo
from utils import drop_db, random_objectid

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

def test_store_user():
    drop_db(DBNAME)
    GTDRepo.add_user(username="user1", password="mypass", email="user@gtd.com")
    users = GTDRepo.get_all_users()
    assert len(users) == 1
    assert users[0].username == "user1"
    assert users[0].password == "mypass"
    assert users[0].email == "user@gtd.com"
    drop_db(DBNAME)


def test_get_user_by_id():
    drop_db(DBNAME)
    GTDRepo.add_user(username="user1", password="mypass", email="user@gtd.com")
    users = GTDRepo.get_all_users()
    assert len(users) == 1
    uid = users[0].id
    stored_user = GTDRepo.get_user_by_id(uid)
    assert stored_user.username == "user1"
    assert stored_user.password == "mypass"
    assert stored_user.email == "user@gtd.com"
    not_stored_user = GTDRepo.get_user_by_id(random_objectid()) #should not be in the database
    assert not_stored_user == None
    drop_db(DBNAME)