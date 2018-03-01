from GTDApp.repo import GTDRepo
from utils import drop_db, random_objectid
import pytest


@pytest.fixture
def resource():
    drop_db("gtd_test") # TODO: read from config?

def test_store_user(resource):
    GTDRepo.add_user(username="user1", password="mypass", email="user@gtd.com")
    users = GTDRepo.get_all_users()
    assert len(users) == 1
    assert users[0].username == "user1"
    assert users[0].password == "mypass"
    assert users[0].email == "user@gtd.com"
    resource


def test_get_user_by_id(resource):
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
    resource


def test_get_user_by_username(resource):
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
    resource
