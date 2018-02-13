from mongoengine import connect, Document, StringField, ListField, ReferenceField

def database_setup(db_name):
    connect(db_name)


class User(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    email = StringField(required=True)


class Item(Document):
    description = StringField(required=True)
    location = StringField(required=True)


class Task(Document):
    description = StringField(required=True)
    status = StringField(required=True)


class Project(Document):
    description = StringField(required=True)
    tasks = ListField(ReferenceField(Task))