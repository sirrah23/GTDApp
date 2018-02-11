from src.repo import GTDRepo
from utils import drop_db

DBNAME = "gtd_test"

def test_store_item():
    drop_db(DBNAME)
    GTDRepo.connect(DBNAME)
    GTDRepo.add_item(description="This is a test", location="inbox")
    assert len(GTDRepo.get_all_items()) == 1
    drop_db(DBNAME)
