from mongoengine import *

def drop_db(db_name):
    db = connect(db_name)
    db.drop_database(db_name)
