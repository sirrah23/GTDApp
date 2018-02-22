from src.repo import GTDRepo
from utils import drop_db, random_objectid

DBNAME = "gtd_test"

#TODO: Add Setup and Teardown for tests

GTDRepo.connect(DBNAME)

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


def test_get_user_by_username():
    drop_db(DBNAME)
    GTDRepo.add_user(username="user1", password="mypass", email="user@gtd.com")
    users = GTDRepo.get_all_users()
    assert len(users) == 1
    uid = users[0].id
    stored_user = GTDRepo.get_user_by_username("user1")
    assert stored_user.id == uid
    assert stored_user.username == "user1"
    assert stored_user.password == "mypass"
    assert stored_user.email == "user@gtd.com"
    not_stored_user = GTDRepo.get_user_by_username("randomuser") #should not be in the database
    assert not_stored_user == None
    drop_db(DBNAME)
