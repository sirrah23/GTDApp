import json
from flask import request
from GTDApp import app
from GTDApp.repo import ItemRepo
from flask_login import login_required, current_user


@app.route("/api/item", methods=["POST"])
@login_required
def item_add():
    uid = current_user.get_obj_id()
    payload = request.get_json()
    if "description" not in payload:
        res = {"success": False}
    else:
        location = payload.get("location", "inbox")
        res = {}
        added_item = ItemRepo.add_item(payload["description"], uid, location=location)
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
    user_items = ItemRepo.get_all_items(user=uid, str_id=True)
    res = {}
    res["success"] = True
    res["data"] = user_items
    return json.dumps(res)


@app.route("/api/item/delete/<item_id>", methods=["POST"])
@login_required
def item_delete(item_id):
    delete_res = ItemRepo.delete_item(item_id)
    return json.dumps({"success": delete_res})


@app.route("/api/item/<item_id>/to-someday", methods=["POST"])
@login_required
def item_to_someday(item_id):
    uid = current_user.get_obj_id()
    item = ItemRepo.item_to_someday(item_id, uid)
    if not item:
        return json.dumps({"success": False})
    else:
        return json.dumps({"success": True, "data": item})


@app.route("/api/item/<item_id>/to-task", methods=["POST"])
@login_required
def item_to_task(item_id):
    uid = current_user.get_obj_id()
    task = ItemRepo.item_to_task(item_id, uid)
    if not task:
        return json.dumps({"success": False})
    else:
        return json.dumps({"success": True, "data": task})


@app.route("/api/item/<item_id>/to-project", methods=["POST"])
@login_required
def item_to_project(item_id):
    uid = current_user.get_obj_id()
    project = ItemRepo.item_to_project(item_id, uid)
    if not project:
        return json.dumps({"success": False})
    else:
        return json.dumps({"success": True, "data": project})
