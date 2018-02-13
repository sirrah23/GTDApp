from .schema import database_setup, Item, Task, Project, User


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

    @classmethod
    def add_project(cls, description, tasks=[]):
        if cls.connected:
            p = Project(description=description, tasks=tasks)
            p.save()
    
    @classmethod
    def get_all_projects(cls):
        if cls.connected:
            return list(Project.objects())
        else:
            return None

    @classmethod
    def add_user(cls, username, password, email):
        if cls.connected:
            u = User(username=username, password=password, email=email)
            u.save()

    @classmethod
    def get_all_users(cls):
        if cls.connected:
            return list(User.objects())
        else:
            return None

    @classmethod
    def get_user_by_id(cls, uid):
        if cls.connected:
            res =  User.objects(id=uid)
            if res.count() > 0:
                return res.first()
            else:
                return None
