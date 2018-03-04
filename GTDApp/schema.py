from mongoengine import connect, Document, StringField, ListField, ReferenceField, BooleanField

def database_setup(db_name):
    connect(db_name)


class User(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    email = StringField(required=True)


class Item(Document):
    description = StringField(required=True)
    location = StringField(required=True)
    user = ReferenceField(User, required=True)


class Task(Document):
    description = StringField(required=True)
    status = StringField(required=True)
    is_project_task = BooleanField(required=True, default=False)
    user = ReferenceField(User, required=True)


class Project(Document):
    description = StringField(required=True)
    tasks = ListField(ReferenceField(Task))
    user = ReferenceField(User, required=True)
