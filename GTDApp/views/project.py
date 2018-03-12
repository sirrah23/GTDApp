import json
from flask import request
from GTDApp import app
from GTDApp.repo import ProjectRepo
from flask_login import login_required, current_user


@app.route("/api/project", methods=["POST"])
@login_required
def project_add():
    uid = current_user.get_obj_id()
    payload = request.get_json()
    if "description" not in payload:
        res = {"success": False}
    else:
        res = {}
        added_project = ProjectRepo.add_project(payload["description"], uid)
        if added_project:
            res["success"] = True
            res["data"] = added_project
        else:
            res["success"] = False
        return json.dumps(res)


@app.route("/api/project/<project_id>/task", methods=["POST"])
@login_required
def project_task_add(project_id):
    uid = current_user.get_obj_id()
    payload = request.get_json()
    if "description" not in payload:
        res = {"success": False}
    else:
        res = {}
        added_task = ProjectRepo.add_project_task(project_id, payload["description"], uid)
        if added_task:
            res["success"] = True
            res["data"] = added_task
        else:
            res["success"] = False
    return json.dumps(res)


@app.route("/api/project/<project_id>/task/<task_id>", methods=["POST"])
@login_required
def project_task_delete(project_id, task_id):
    uid = current_user.get_id()
    res = ProjectRepo.delete_project_task(project_id, task_id, uid)
    return json.dumps({"success": res})


@app.route("/api/project", methods=["GET"])
@login_required
def project_get():
    uid = current_user.get_obj_id()
    user_projects = ProjectRepo.get_all_projects(user=uid)
    res = {}
    if user_projects:
        res["success"] = True
        res["data"] = user_projects
    else:
        res["success"] = False
        res["data"] = {}
    return json.dumps(res)


@app.route("/api/project/delete/<project_id>", methods=["POST"])
@login_required
def project_delete(project_id):
    delete_res = ProjectRepo.delete_project(project_id)
    return json.dumps({"success": delete_res})
