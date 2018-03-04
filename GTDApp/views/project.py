import json
from flask import request
from GTDApp import app
from GTDApp.repo import GTDRepo
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
        added_project = GTDRepo.add_project(payload["description"], uid)
        if added_project:
            res["success"] = True
            res["data"] = added_project
        else:
            res["success"] = False
        return json.dumps(res)


@app.route("/api/project", methods=["GET"])
@login_required
def project_get():
    uid = current_user.get_obj_id()
    user_projects = GTDRepo.get_all_projects(user=uid)
    res = {}
    if user_projects:
        res["success"] = True
        res["data"] = user_projects
    else:
        res["success"] = False
        res["data"] = {}
    return json.dumps(res)
