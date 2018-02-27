import json
from flask import request
from GTDApp import app
from GTDApp.repo import GTDRepo
from flask_login import login_required, current_user


@app.route("/api/item", methods=["POST"])
@login_required
def item_add():
    uid = current_user.get_obj_id()
    payload = request.get_json()
    if "description" not in payload:
        res = {"success": False}
    else:
        res = {}
        added_item = GTDRepo.add_item(payload["description"], uid, str_id=True)
        if added_item:
            res["success"] = True
            res["data"] = added_item
        else:
            res["success"] = False
    return json.dumps(res)


@app.route("/api/item", methods=["GET"])
@login_required
def item_get():
    uid = current_user.get_obj_id()
    user_items = GTDRepo.get_all_items(user=uid, str_id=True)
    res = {}
    res["success"] = True
    res["data"] = user_items
    return json.dumps(res)
