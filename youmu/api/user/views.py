__author__ = 'badpoet'

import json
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort)
from flask.ext.login import (login_required, current_user, login_user, logout_user, confirm_login)

from .service import UserService
import json
import os
import mimetypes
from werkzeug.utils import secure_filename
from tempfile import mktemp
import random
import string

user = Blueprint("user", __name__, url_prefix = "/api/user")

# tests begin

@user.route("/_tell", methods = ["GET", "POST"])
def tell():
    if current_user.is_anonymous():
        return "You are a tourist."
    else:
        return "You are " + current_user.name

@user.route("/_transform", methods = ["GET"])
def transform():
    if current_user.is_anonymous():
        return "failed"
    UserService.transform_admin(current_user.id)
    return "transformed"

# tests end

@user.route("/_login", methods = ["POST"])
def login():
    postBody = json.loads(request.data)
    id = postBody["username"]
    password = postBody["password"]
    user = UserService.authenticate(id, password)
    if user is not None:
        login_user(user)
        return '{"state": "ok"}'
    return '{"state": "failed"}'

@user.route("/_logout", methods = ["POST"])
def logout():
    logout_user()
    return '{"state": "ok"}'

@user.route("/_me", methods = ["GET"])
def me():
    if current_user.is_anonymous():
        return ""
    return json.dumps(UserService.load_user_by_id(current_user.id).to_dict(), ensure_ascii = False)

@user.route("/_me", methods = ["PUT"])
def update_me():
    if current_user.is_anonymous():
        return ""
    body = request.form
    name = body["name"]
    try:
        user_of_name = UserService.get_user_by_name(name)

        # If we get here, the name is taken
        if user_of_name.id != current_user.id:
            return json.dumps({"state":"fail", "content":"name is taken"}, ensure_ascii = False)
    except Exception, e:
        pass

    try:
        UPLOAD_FOLDER = "youmu/static/uploads/images/"
        ALLOWED_MIMETYPES = ("image/png", "image/jpeg", "image/jpg", "image/bmp")
        f = request.files["avatar"]
        fname = f.filename.encode("ascii", "xmlcharrefreplace")
        pname = mktemp(suffix='_', prefix='u', dir=UPLOAD_FOLDER) + secure_filename(fname)
        f.save(pname)
        if mimetypes.guess_type(pname)[0] not in ALLOWED_MIMETYPES:
            os.remove(pname)
            return json.dumps({"state":"fail", "content":"wrong mime type"}, ensure_ascii = False)
        pname = str(pname)
        avatar = pname[pname.find("/"):]
    except Exception, e:
        print e
        avatar = ""
    msg = UserService.update(current_user.id, name, avatar)
    return json.dumps({ "state": msg })

@user.route("/<user_id>/_disable", methods = ["POST"])
def disable_user(user_id):
    if current_user.is_anonymous() or not current_user.is_admin():
        return '{ "state": "need admin" }'
    res = UserService.disable(user_id, True)
    return json.dumps({ "state": "ok" if res else "failed" })

@user.route("/<user_id>/_enable", methods = ["POST"])
def enable_user(user_id):
    if current_user.is_anonymous() or not current_user.is_admin():
        return '{ "state": "need admin" }'
    res = UserService.disable(user_id, False)
    return json.dumps({ "state": "ok" if res else "failed" })

@user.route("/", methods = ["GET"])
def list_users():
    if current_user.is_anonymous() or not current_user.is_admin():
        return '{ "state": "need admin" }'
    offset = request.args.get('offset', 0)
    size = request.args.get('size', 10)
    raw = UserService.list_users(offset, size)
    raw["result"] = [u.to_dict() for u in raw["result"]]
    return json.dumps(raw, ensure_ascii = False)

@user.route("/<user_id>", methods = ["GET"])
def get_user(user_id):
    if current_user.is_anonymous() or not current_user.is_admin():
        return '{ "state": "need admin" }'
    return json.dumps(UserService.load_user_by_id(user_id).to_dict(), ensure_ascii = False)

@user.route("/<user_id>/_toggle-admin", methods = ["POST"])
def toggle_user_is_admin(user_id):
    UserService.transform_admin(user_id)
    return json.dumps({ "state": "ok" })

@user.route("/name/<user_name>", methods = ["GET"])
def get_user_by_name(user_name):
    return json.dumps(UserService.get_user_by_name(user_name).to_dict(), ensure_ascii = False)
