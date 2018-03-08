from bson import ObjectId
from .schema import database_setup, Item, Task, Project, User


"""
TODO: Come up with a generic way to transform mongoengine objects
into their dictionary form
"""


class GTDRepo:

    connected = False

    @classmethod
    def connect(cls, db_name):
        database_setup(db_name)
        cls.connected = True

    @classmethod
    def add_item(cls, description, user, location="inbox"):
        if not cls.connected:
            return
        i = Item(description=description, location=location, user=user)
        i.save()
        res = {}
        res["id"] = str(i.id)
        res["description"] = description
        res["location"] = location
        return res

    @classmethod
    def delete_item(cls, item_id):
        if not cls.connected:
            return False
        if not ObjectId.is_valid(item_id):
            return False
        item = Item.objects(id=item_id)
        if len(item) != 1:
            return False
        item.delete()
        return True

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
    def item_to_someday(cls, item_id, user_id):
        if not cls.connected:
            return None
        if not ObjectId.is_valid(item_id) or not ObjectId.is_valid(user_id):
            return None
        item = Item.objects(id=item_id, user=user_id).first()
        if not item:
            return None
        item.location = "someday/maybe"
        item.save()
        res = ({"id": str(item.id),
                "description": item.description,
                "location": item.location})
        return res


    @classmethod
    def item_to_task(cls, item_id, user_id):
        if not cls.connected:
            return None
        if not ObjectId.is_valid(item_id) or not ObjectId.is_valid(user_id):
            return None
        item = Item.objects(id=item_id, user=user_id).first()
        if not item:
            return None
        description = item.description
        task = cls.add_task(description, user_id, str_id=True)
        if not task:
            return None
        item.delete()
        return task

    @classmethod
    def item_to_project(cls, item_id, user_id):
        if not cls.connected:
            return None
        if not ObjectId.is_valid(item_id) or not ObjectId.is_valid(user_id):
            return None
        item = Item.objects(id=item_id, user=user_id).first()
        if not item:
            return None
        description = item.description
        project = cls.add_project(description, user_id)
        if not project:
            return None
        item.delete()
        return project

    @classmethod
    def add_task(cls, description, user, status="todo", project=False, str_id=False):
        if not cls.connected:
            return
        t = Task(description=description, user=user, status=status, is_project_task=project)
        t.save()
        res = {}
        res["id"] = t.id if not str_id else str(t.id)
        res["description"] = description
        res["status"] = status
        return res

    @classmethod
    def get_task(cls, task_id, user=None):
        if not cls.connected:
            return None
        if not ObjectId.is_valid(task_id):
            return None
        if not user:
            task = Task.objects(id=task_id).first()
        else:
            task = Task.objects(user=user, id=task_id).first()
        return ({"id": str(task.id),
                "description": task.description,
                "status": task.status})

    @classmethod
    def get_all_tasks(cls, project= False, user=None):
        if not cls.connected:
            return None
        if not user:
            tasks = Task.objects(is_project_task=project)
        else:
            tasks = Task.objects(is_project_task=project, user=user)
        res = []
        for task in tasks:
            res.append({
                "id": str(task.id),
                "description": task.description,
                "status": task.status
            })
        return res

    @classmethod
    def toggle_task(cls, task_id):
        if not cls.connected:
            return None
        if not ObjectId.is_valid(task_id):
            return False
        task = Task.objects(id=task_id).first()
        # TODO: Is there a way to stuff this logic into the Task object itself?
        if task.status == "todo":
            task.status = "done"
        else:
            task.status = "todo"
        task.save()
        return True

    @classmethod
    def delete_task(cls, task_id, user_id):
        if not cls.connected:
            return False
        if not ObjectId.is_valid(task_id) or not ObjectId.is_valid(user_id):
            return False
        task_to_del = Task.objects(id=task_id, user=user_id).first()
        if not task_to_del:
            return False
        task_to_del.delete()
        return True

    @classmethod
    def task_to_project(cls, task_id, user_id):
        if not cls.connected:
            return None
        if not ObjectId.is_valid(task_id) or not ObjectId.is_valid(user_id):
            return None
        task = Task.objects(id=task_id, user=user_id).first()
        if not task:
            return None
        description = task.description
        project = cls.add_project(description, user_id)
        if not project:
            return None
        task.delete()
        return project

    @classmethod
    def add_project(cls, description, user, tasks=[]):
        if not cls.connected:
            return
        p = Project(description=description, tasks=tasks, user=user)
        p.save()
        res = {}
        res["id"] = str(p.id)
        res["description"] = p.description
        res["tasks"] = [{"id": str(task.id),
                         "description": task.description,
                         "status": task.status} for task in p.tasks] #TODO: Duplicated code
        return res

    @classmethod
    def get_all_projects(cls, user=None):
        if not cls.connected:
            return None
        if not user:
            projects = Project.objects()
        else:
            projects = Project.objects(user=user)
        res = []
        for project in projects:
            res.append({
                "id": str(project.id),
                "description": project.description,
                "tasks": [{"id": str(task.id),
                           "description": task.description,
                           "status": task.status}
                          for task in project.tasks]
            })
        return res

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

    @classmethod
    def add_project_task(cls, project_id, description, user_id):
        if not cls.connected:
            return
        if not ObjectId.is_valid(project_id) or not ObjectId.is_valid(user_id):
            return
        p = Project.objects(id=project_id, user=user_id).first()
        if not p:
            return
        t = cls.add_task(description, user_id, project=True, str_id=True)
        p.tasks.append(ObjectId(t["id"]))
        p.save()
        return t


    @classmethod
    def delete_project_task(cls, project_id, task_id, user_id):
        if not cls.connected:
            return
        if (not ObjectId.is_valid(project_id)
            or not ObjectId.is_valid(task_id)
            or not ObjectId.is_valid(user_id)):
            return False
        proj = Project.objects(id=project_id, user=user_id).first()
        if not proj:
            return
        toid = ObjectId(task_id)
        del_task = None
        new_proj_tasks = []
        for task in proj.tasks:
            if task.id == toid:
                del_task = task
            else:
                new_proj_tasks.append(task)
        if not del_task: # The task we wanted to delete does not exist
            return False
        proj.tasks = new_proj_tasks
        del_task.delete() # Actually delete the task we wanted to delete
        proj.save() # Update project to remove reference to deleted task
        print("Successfully removed the one task")
        return True


    @classmethod
    def delete_project(cls, project_id):
        if not cls.connected:
            return False
        if not ObjectId.is_valid(project_id):
            return False
        project = Project.objects(id=project_id).first()
        if not project:
            return False
        project_tasks = project.tasks
        # Delete the project
        project.delete()
        # Delete all sub-tasks under the project
        for project_task in project_tasks:
            project_task.delete()
        return True
