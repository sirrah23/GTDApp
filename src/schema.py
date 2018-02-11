from mongoengine import *


def database_setup(db_name):
    connect(db_name)


class Item(Document):
    description = StringField(required=True)
    location = StringField(required=True)
