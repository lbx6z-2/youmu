__author__ = 'badpoet'

from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, Response)
from flask.ext.login import (login_required, current_user, login_user, logout_user, confirm_login)
import json
import datetime
from youmu.models.barrage import Barrage
from youmu.api.barrage.service import BarrageService

barrage = Blueprint("barrage", __name__, url_prefix = "/api/barrage")

@barrage.route("/video/<video_id>", methods = ["GET"])
def get_video_barrage(video_id):
    r = BarrageService.get_barrage_on_video(video_id)
    return Response(BarrageService.obj_list_to_xml(r), content_type = 'text/xml; charset=utf-8')

@barrage.route("/video/<video_id>", methods = ["POST"])
def post_video_barrage(video_id):
    post_body = json.loads(request.data)
    if current_user.is_anonymous():
        return '{ "state": "need login" }'
    if (not "content" in post_body) or len(post_body.get("content")) == 0:
        return '{ "state": "empty content" }'
    b = Barrage(
        video_id,
        current_user.id,
        post_body.get("content"),
        post_body.get("position"),
        post_body.get("mode"),
        post_body.get("size"),
        post_body.get("color"),
        post_body.get("pool"),
        datetime.datetime.now()
    )
    BarrageService.add_barrage(b)
    return '{ "state": "ok" }'