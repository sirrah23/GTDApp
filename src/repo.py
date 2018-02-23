from .schema import database_setup, Item, Task, Project, User


class GTDRepo:

    connected = False

    @classmethod
    def connect(cls, db_name):
        database_setup(db_name)
        cls.connected = True

    @classmethod
    def add_item(cls, description, user, location="inbox", str_id=False):
        if not cls.connected:
            return
        i = Item(description=description, location=location, user=user)
        i.save()
        res = {}
        res["id"] = i.id if not str_id else str(i.id)
        res["description"] = description
        res["location"] = location
        return res

    @classmethod
    def get_all_items(cls, user=None, str_id=False):
        if not cls.connected:
            return None
        if not user:
            items = Item.objects()
        else:
            items = Item.objects(user=user)
        res = []
        for item in items:
            res.append({
                "id": item.id if not str_id else str(item.id),
                "description": item.description,
                "location": item.location
            })
        return res

    @classmethod
    def add_task(cls, description, user, status="todo"):
        if cls.connected:
            t = Task(description=description, status=status, user=user)
            t.save()

    @classmethod
    def get_all_tasks(cls):
        if cls.connected:
            return list(Task.objects())
        else:
            return None

    @classmethod
    def add_project(cls, description, user, tasks=[]):
        if cls.connected:
            p = Project(description=description, tasks=tasks, user=user)
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

    @classmethod
    def get_user_by_username(cls, username):
        if cls.connected:
            res =  User.objects(username=username)
            if res.count() > 0:
                return res.first()
            else:
                return None
