import json
from flask import request
from GTDApp import app
from GTDApp.repo import GTDRepo
from flask_login import login_required, current_user


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
