from .schema import database_setup, Item, Task


class GTDRepo:

    connected = False

    @classmethod
    def connect(cls, db_name):
        database_setup(db_name)
        cls.connected = True

    @classmethod
    def add_item(cls, description, location="inbox"):
        if cls.connected:
            i = Item(description=description, location=location)
            i.save()

    @classmethod
    def get_all_items(cls):
        if cls.connected:
            return list(Item.objects())
        else:
            return None

    @classmethod
    def add_task(cls, description, status="todo"):
        if cls.connected:
            t = Task(description=description, status=status)
            t.save()
    
    @classmethod
    def get_all_tasks(cls):
        if cls.connected:
            return list(Task.objects())
        else:
            return None