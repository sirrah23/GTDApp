import json
from flask import request
from GTDApp import app
from GTDApp.repo import TaskRepo
from flask_login import login_required, current_user


@app.route("/api/task", methods=["POST"])
@login_required
def task_add():
    uid = current_user.get_obj_id()
    payload = request.get_json()
    if "description" not in payload:
        res = {"success": False}
    else:
        res = {}
        added_task = TaskRepo.add_task(payload["description"], uid)
        if added_task:
            res["success"] = True
            res["data"] = added_task
        else:
            res["success"] = False
    return json.dumps(res)


@app.route("/api/task", methods=["GET"])
@login_required
def task_get():
    uid = current_user.get_obj_id()
    user_tasks = TaskRepo.get_all_tasks(user=uid)
    res = {}
    res["success"] = True
    res["data"] = user_tasks
    return json.dumps(res)


# TODO: Use the actual delete method here
@app.route("/api/task/<task_id>/delete", methods=["POST"])
@login_required
def task_delete(task_id):
    uid = current_user.get_obj_id()
    res = TaskRepo.delete_task(task_id, uid)
    return json.dumps({"success": res})


# TODO: Use the actual update method here
@app.route("/api/task/update/<task_id>", methods=["POST"])
@login_required
def task_update(task_id):
    res = TaskRepo.toggle_task(task_id)
    if not res:
        return json.dumps({"success": False})
    task = TaskRepo.get_task(task_id)
    if task:
        return json.dumps({"success": True, "data": task})
    else:
        return json.dumps({"success": True})


@app.route("/api/task/<task_id>/to-project", methods=["POST"])
@login_required
def task_to_project(task_id):
    uid = current_user.get_obj_id()
    project = TaskRepo.task_to_project(task_id, uid)
    if not project:
        return json.dumps({"success": False})
    else:
        return json.dumps({"success": True, "data": project})
