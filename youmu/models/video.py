__author__ = 'badpoet'

import json

from youmu.clients import mongo
from youmu.api.user.service import UserService

class Video(object):

    VIDEO = "video"
    AUDIO = "audio"
    LIVE = "live"
    MEDIA_TYPES = [VIDEO, AUDIO, LIVE]

    def __init__(self, video_id = "", title = "", cover = "", description = "",
                 play_count = 0, like = 0, owner_id = "", disabled = False,
                 banned = False, upload_time = "", length = 0, tags = (),
                 category = "", media_type = VIDEO, url = ""):
        self.video_id = unicode(video_id)
        self.title = title
        self.cover = cover if len(cover) > 0 else "http://placehold.it/1000x1000&amp;text=Thumbnail"
        self.description = description
        self.play_count = int(play_count)
        self.like = int(like)
        self.owner_id = owner_id
        self.disabled = disabled
        self.banned = banned
        self.upload_time = upload_time
        self.length = int(length)
        self.tags = tags
        self.category = category
        self.media_type = media_type
        self.url = url

    def to_dict(self):
        dic = {
            "video_id": self.video_id,
            "title": self.title,
            "cover": self.cover,
            "description": self.description,
            "play_count": self.play_count,
            "like": self.like,
            "owner_id": self.owner_id,
            "disabled": self.disabled,
            "banned": self.banned,
            "upload_time": self.upload_time,
            "length": self.length,
            "tags": self.tags,
            "category": self.category,
            "media_type": self.media_type,
            "url": self.url
        }
        return dic

    def to_rich_dict(self):
        dic = self.to_dict()
        user = UserService.load_user_by_id(self.owner_id)
        dic["owner_name"] = user.name
        dic["owner_avatar"] = user.avatar
        return dic

    def valid(self, user_id):
        if mongo.check_admin(user_id):
            return True
        if self.banned:
            return False
        if self.owner_id == user_id:
            return True
        return not self.disabled

