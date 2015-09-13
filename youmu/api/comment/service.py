__author__ = 'badpoet'

from youmu.models.comment import Comment
from youmu.clients import mongo
from datetime import datetime

class CommentService(object):

    @staticmethod
    def mto(item):
        return Comment(
            item.get("comment_id"),
            item.get("user_id"),
            item.get("video_id"),
            item.get("content"),
            item.get("reply_to"),
            item.get("reply_time"),
            int(item.get("floor"))
        )

    @staticmethod
    def comment_on(user_id, video_id, content, reply_to = ""):
        floor = mongo.assign_comment_floor(video_id)
        mongo.insert_comment({
            "comment_id": video_id + ":" + str(floor),
            "user_id": user_id,
            "video_id": video_id,
            "content": content,
            "floor": floor,
            "reply_to": reply_to,
            "reply_time": datetime.now()
        })

    @staticmethod
    def get_comments_by_video_id(video_id, offset, size):
        return [CommentService.mto(item) for item in mongo.get_comment_by_video_id(video_id, offset, size)]

    @staticmethod
    def get_comments_by_user_id(user_id, offset, size, reverse):
        return [CommentService.mto(item) for item in mongo.get_comment_by_user_id(user_id, offset, size, reverse)]

    @staticmethod
    def remove_comment_by_id(comment_id, current_id, is_admin = False):
        d = mongo.get_comment_by_comment_id(comment_id)
        if d is None:
            return False
        if (not is_admin) and (CommentService.mto(d).user_id != current_id):
            return False
        mongo.remove_comment_by_id(comment_id)
        return True