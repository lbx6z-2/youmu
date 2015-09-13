__author__ = 'badpoet'

from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort)

from flask.ext.login import (login_required, current_user, login_user, logout_user, confirm_login)
from .service import VideoListService

import json

video_list = Blueprint("videolist", __name__, url_prefix = "/api/videolist")

@video_list.route("/", methods = ["GET"])
def general_query():
    offset = request.args.get('offset', 0)
    size = request.args.get('size', 10)
    order_by = request.args.get('order_by', "upload_time")
    reverse = request.args.get('reverse', 0) > 0
    res = VideoListService.general_get(offset, size, order_by, reverse,
                                       show_banned = (not current_user.is_anonymous()) and current_user.is_admin(),
                                       show_disabled = (not current_user.is_anonymous()) and current_user.is_admin())
    res = [v.to_rich_dict() for v in res]
    return json.dumps(res, ensure_ascii = False)

@video_list.route("/_search", methods = ["GET"])
def adv_search():
    kw = request.args.get('keyword', "")
    res = VideoListService.adv_search(kw) if kw else []
    res = [v.to_rich_dict() for v in res]
    return json.dumps(res, ensure_ascii = False)

@video_list.route("/owner/<owner_id>", methods = ["GET"])
def query_on_owner(owner_id):
    offset = request.args.get('offset', 0)
    size = request.args.get('size', 10)
    order_by = request.args.get('order_by', "upload_time")
    reverse = request.args.get('reverse', 0) > 0
    res = VideoListService.get_with_owner(owner_id, offset, size, order_by, reverse,
                                          show_banned = (not current_user.is_anonymous()) and current_user.is_admin(),
                                          show_disabled = current_user.id == owner_id)
    res = [v.to_rich_dict() for v in res]
    return json.dumps(res, ensure_ascii = False)

@video_list.route("/title/<title>", methods = ["GET"])
def query_on_title(title):
    offset = request.args.get('offset', 0)
    size = request.args.get('size', 10)
    order_by = request.args.get('order_by', "upload_time")
    reverse = request.args.get('reverse', 0) > 0
    res = VideoListService.query_on_title(title, offset, size, order_by, reverse,
                                          show_banned = (not current_user.is_anonymous()) and current_user.is_admin(),
                                          show_disabled = (not current_user.is_anonymous()) and current_user.is_admin())
    res = [v.to_rich_dict() for v in res]
    return json.dumps(res, ensure_ascii = False)

@video_list.route("/owner_name/<owner_name>", methods = ["GET"])
def query_on_owner_name(owner_name):
    offset = request.args.get('offset', 0)
    size = request.args.get('size', 10)
    order_by = request.args.get('order_by', "upload_time")
    reverse = request.args.get('reverse', 0) > 0
    res = VideoListService.query_on_owner_name(owner_name, offset, size, order_by, reverse,
                                          show_banned = (not current_user.is_anonymous()) and current_user.is_admin(),
                                          show_disabled = (not current_user.is_anonymous()) and current_user.is_admin())
    res = [v.to_rich_dict() for v in res]
    return json.dumps(res, ensure_ascii = False)

@video_list.route("/description/<description>", methods = ["GET"])
def query_on_description(description):
    offset = request.args.get('offset', 0)
    size = request.args.get('size', 10)
    order_by = request.args.get('order_by', "upload_time")
    reverse = request.args.get('reverse', 0) > 0
    res = VideoListService.query_on_description(description, offset, size, order_by, reverse,
                                          show_banned = (not current_user.is_anonymous()) and current_user.is_admin(),
                                          show_disabled = (not current_user.is_anonymous()) and current_user.is_admin())
    res = [v.to_rich_dict() for v in res]
    return json.dumps(res, ensure_ascii = False)
