__author__ = 'badpoet'

from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort)

from flask.ext.login import (login_required, current_user, login_user, logout_user, confirm_login)
from youmu.models.video import Video
from .service import VideoService
from youmu.api.videolist.service import VideoListService

import json
import time
import os
import mimetypes
from werkzeug.utils import secure_filename
from tempfile import mktemp

video = Blueprint("video", __name__, url_prefix = "/api/video")


@video.route("/", methods = ["GET"])
def get_video_list():
    videos = VideoListService.general_get(offset = 0, size = 10, order_by = "upload_time", reverse = True,
                                       show_banned = (not current_user.is_anonymous()) and current_user.is_admin(),
                                       show_disabled = (not current_user.is_anonymous()) and current_user.is_admin())
    videos = [video.to_rich_dict() for video in videos]
    return json.dumps(videos, ensure_ascii = False)


@video.route("/<video_id>", methods = ["GET"])
def get_video_by_id(video_id):
    v = VideoService.get_video_by_id(video_id)
    if v:
        if current_user.is_anonymous() or v.valid(current_user.id):
            v = v.to_rich_dict()
        else:
            v = None
    return json.dumps(v, ensure_ascii = False)


@video.route("/<video_id>/_disable", methods = ["POST"])
def hide_video(video_id):
    res = VideoService.hide_video(video_id, current_user.id, op = True)
    return json.dumps({"state":"success" if res else "failed"})


@video.route("/<video_id>/_ban", methods = ["POST"])
def ban_video(video_id):
    res = VideoService.ban_video(video_id, (not current_user.is_anonymous()) and current_user.is_admin(), op = True)
    return json.dumps({"state":"success" if res else "failed"})


@video.route("/<video_id>/_enable", methods = ["POST"])
def show_video(video_id):
    res = VideoService.hide_video(video_id, current_user.id, op = False)
    return json.dumps({"state":"success" if res else "failed"})


@video.route("/<video_id>/_unban", methods = ["POST"])
def unban_video(video_id):
    res = VideoService.ban_video(video_id, (not current_user.is_anonymous()) and current_user.is_admin(), op = False)
    return json.dumps({"state":"success" if res else "failed"})


@video.route("/<video_id>/_play", methods = ["POST"])
def add_play_count(video_id):
    VideoService.add_play_count(video_id)
    return ""


@video.route("/<video_id>/_like", methods = ["GET", "POST"])
def like(video_id):
    if request.method == "GET":
        data = { "total": VideoService.count_like_info_by_video(video_id) }
        return json.dumps(data, ensure_ascii = False)
    if request.method == "POST":
        if not current_user.is_anonymous():
            VideoService.click_like(current_user.id, video_id)
        return is_liked_by_me(video_id)


@video.route("/<video_id>/_like/<user_id>", methods = ["GET"])
def is_liked_by_user(video_id, user_id):
    state = VideoService.has_liked(user_id, video_id)
    return json.dumps({ "like": "yes" if state else "no" }, ensure_ascii = False)


@video.route("/<video_id>/_like/_me", methods = ["GET"])
def is_liked_by_me(video_id):
    if current_user.is_anonymous():
        return '{"like": "no"}'
    state = VideoService.has_liked(current_user.id, video_id)
    return json.dumps({ "like": "yes" if state else "no" }, ensure_ascii = False)


@video.route("/upload", methods = ["POST"])
def upload_video():
    if current_user.is_anonymous():
        return '{"state":"fail"}'
    postBody = request.form
    live = postBody.get("live", "0") == "0"
    if live:
        # video
        try:
            UPLOAD_FOLDER = "youmu/static/uploads/videos/"
            ALLOWED_MIMETYPES = ("video/mp4", "video/x-matroska", "audio/mpeg")
            f = request.files["video"]
            ascii_name = f.filename.encode("ascii", "xmlcharrefreplace")
            fname = mktemp(suffix='_', prefix='u', dir=UPLOAD_FOLDER) + secure_filename(ascii_name)
            f.save(fname)
            mime_type = mimetypes.guess_type(fname)[0]
            if mime_type not in ALLOWED_MIMETYPES:
                os.remove(fname)
                return json.dumps({"state":"fail", "content":"wrong mime type"}, ensure_ascii = False)
            fname = str(fname)
            fname = fname[fname.find("/"):]
            media_type = "audio" if mime_type.find("mp3") != -1 else "video"
        except:
            return json.dumps({"state":"fail", "content":"video/audio upload failed"}, ensure_ascii = False)
        url = ""
    else:
        media_type = "live"
        url = postBody.get("rtmp", "")
        fname = ""
    # cover
    try:
        UPLOAD_FOLDER = "youmu/static/uploads/images/"
        ALLOWED_MIMETYPES = ("image/png", "image/jpeg", "image/jpg", "image/bmp")
        f = request.files["cover"]
        ascii_name = f.filename.encode("ascii", "xmlcharrefreplace")
        pname = mktemp(suffix='_', prefix='u', dir=UPLOAD_FOLDER) + secure_filename(ascii_name)
        f.save(pname)
        if mimetypes.guess_type(pname)[0] not in ALLOWED_MIMETYPES:
            os.remove(pname)
            return json.dumps({"state":"fail", "content":"wrong mime type"}, ensure_ascii = False)
        pname = str(pname)
        pname = pname[pname.find("/"):]
    except:
        pname = ""
    # other information
    category = postBody.get("category", "")
    if not category in VideoService.get_categories(): category = ""
    obj = Video(owner_id = current_user.id,
        title = postBody["title"],
        upload_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
        cover = pname,
        category = category,
        description = postBody["description"],
        media_type = media_type,
        url = url)
    VideoService.insert_video(obj, fname)
    return json.dumps({"state":"success"}, ensure_ascii = False)


@video.route("/file/<video_id>/WAIMAIdi2fen0.5price")
def get_file_name(video_id):
    return VideoService.get_file_name(video_id)

@video.route("/_categories", methods = ["GET"])
def get_categories():
    return json.dumps({"categories": VideoService.get_categories()})
