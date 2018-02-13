from mongoengine import *
from datetime import datetime
from bson.objectid import ObjectId

def drop_db(db_name):
    db = connect(db_name)
    db.drop_database(db_name)

def random_objectid():
    return ObjectId.from_datetime(datetime.now())