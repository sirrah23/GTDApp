import json
from flask import request
from GTDApp import app
from GTDApp.repo import GTDRepo
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
        added_task = GTDRepo.add_task(payload["description"], uid, str_id=True)
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
    user_tasks = GTDRepo.get_all_tasks(user=uid)
    res = {}
    res["success"] = True
    res["data"] = user_tasks
    return json.dumps(res)


@app.route("/api/task/update/<task_id>", methods=["POST"])
@login_required
def task_update(task_id):
    res = GTDRepo.toggle_task(task_id)
    if not res:
        return json.dumps({"success": False})
    task = GTDRepo.get_task(task_id)
    if task:
        return json.dumps({"success": True, "data": task})
    else:
        return json.dumps({"success": True})

