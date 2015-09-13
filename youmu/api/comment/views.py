__author__ = 'badpoet'

from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort)

from flask.ext.login import (login_required, current_user, login_user, logout_user, confirm_login)
from .service import CommentService

import json

comment = Blueprint("comment", __name__, url_prefix = "/api/comment")

@comment.route("/video/<video_id>", methods = ["GET", "POST"])
def work_on_video(video_id):
    if request.method == "GET":
        offset = int(request.args.get("offset", 0))
        size = int(request.args.get("size", 20))

        comments = [c.to_rich_dict() for c in CommentService.get_comments_by_video_id(video_id, offset, size)]
        return json.dumps(comments, ensure_ascii = False)
    else:
        if current_user.is_anonymous():
            return '{ "state": "need login" }'
        body = json.loads(request.data)
        content = body.get("content", "")
        if not content:
            return '{ "state": "empty content" }'
        CommentService.comment_on(current_user.id, video_id, content, "")
        return '{ "state": "ok" }'

@comment.route("/user/<user_id>", methods = ["GET"])
def work_on_user(user_id):
    offset = int(request.args.get("offset", 0))
    size = int(request.args.get("size", 20))
    reverse = int(request.args.get("reverse", 0)) > 0
    comments = [c.to_rich_dict() for c in CommentService.get_comments_by_user_id(user_id, offset, size, reverse)]
    return json.dumps(comments, ensure_ascii = False)

@comment.route("/<comment_id>", methods = ["DELETE"])
def delete_comment(comment_id):
    if (current_user.is_anonymous()):
        return '{ "state": "failed" }'
    if CommentService.remove_comment_by_id(comment_id, current_user.id, current_user.is_admin()):
        return '{ "state": "ok" }'
    else:
        return '{ "state": "failed" }'