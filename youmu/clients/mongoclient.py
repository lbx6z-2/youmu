__author__ = 'badpoet'

import pymongo
from bson.objectid import ObjectId

from youmu.config import DefaultConfig

class MongoClient(object):

    def __init__(self,
                 host = DefaultConfig.MONGO_HOST,
                 port = DefaultConfig.MONGO_PORT,
                 username = DefaultConfig.MONGO_USERNAME,
                 password = DefaultConfig.MONGO_PASSWORD):
        self.db = pymongo.Connection(host, port)["youmu"]
        self.db.authenticate(username, password)
        self.user_col = self.db["user"]
        self.admin_col = self.db["admin_user"]
        self.video_col = self.db["video"]
        self.video_file_col = self.db["video_file"]
        self.video_trash_col = self.db["video_trash"]
        self.video_like_col = self.db["video_like"]
        self.video_cate_col = self.db["video_category"]
        self.comment_col = self.db["comment"]
        self.comment_trash_col = self.db["comment_trash"]
        self.comment_floor_ctrl_col = self.db["floor_ctrl"]
        self.inc_id_ctrl_col = self.db["inc_id_ctrl"]
        self.barrage_col = self.db["barrage"]

    # ABOUT USER

    def has_user_id(self, user_id):
        return self.user_col.find_one({"id": user_id}) is not None

    def get_user_by_id(self, user_id):
        return self.user_col.find_one({"id": user_id})

    def get_user_by_mid(self, user_mongo_id):
        return self.user_col.find_one({"_id": ObjectId(user_mongo_id)})

    def get_user_by_name(self, user_name):
        return self.user_col.find_one({"name": user_name})

    def list_users(self, offset = 0, size = 10):
        return self.user_col.find()[offset : size]

    def count_users(self):
        return self.user_col.find().count()

    def insert_user(self, user_dict):
        self.user_col.insert(user_dict)

    def update_user(self, user_dict):
        self.user_col.update(
            { "_id": user_dict["_id"] },
            user_dict
        )

    def transform_admin(self, user_id):
        if self.admin_col.find_one({ "id": user_id }):
            self.admin_col.remove({ "id": user_id })
        else:
            self.admin_col.insert({ "id": user_id })

    def check_admin(self, user_id):
        return self.admin_col.find_one({ "id": user_id }) is not None

    def disable_user(self, user_id, state = True):
        self.user_col.update(
            { "id": user_id },
            { "$set": { "disabled": state } }
        )

    # ABOUT VIDEO

    def assign_video_id(self):
        tmp = self.inc_id_ctrl_col.find_and_modify(
            query = { "type": "video_id" },
            update = { "$inc": { "video_id": 1 } },
            new = True,
            upsert = True
        )
        return str(tmp["video_id"])

    def get_video_file_name(self, video_id):
        d = self.video_file_col.find_one({"video_id": video_id })
        if d is None:
            return ""
        return d["file_name"]

    def insert_video(self, video, file_name):
        self.video_col.insert(video)
        self.video_file_col.insert( { "video_id": video["video_id"], "file_name": file_name } )

    def get_video_by_id(self, video_id):
        return self.video_col.find_one({"video_id": video_id})

    def hide_video(self, video_id, op = True):
        self.video_col.update(
            { "video_id": video_id },
            { "$set": { "disabled": op } }
        )

    def ban_video(self, video_id, op = True):
        self.video_col.update(
            { "video_id": video_id },
            { "$set": { "banned": op } }
        )

    def get_video_list(self, offset = 0, size = 10):
        return self.video_col.find()[offset : size]

    def get_ordered_video_list(self, query, offset = 0, size = 10, order_by = "upload_time", reverse = False):
        query = {
            "$query": query,
            "$orderby": { order_by: -1 if reverse else 1 }
        }
        return self.video_col.find(query)[offset : size]

    def add_video_play_count(self, id):
        self.video_col.update(
            { "video_id": id },
            { "$inc": { "play_count": 1 } }
        )

    def get_video_categories(self):
        res = [e for e in self.video_cate_col.find()]
        return res

    # ABOUT LIKE

    def create_like_info(self, user_id, video_id):
        self.video_like_col.insert(
            { "user_id": user_id, "video_id": video_id }
        )
        self.video_col.update(
            { "video_id": video_id },
            { "$inc": { "like": 1 } }
        )

    def delete_like_info(self, user_id, video_id):
        self.video_like_col.remove(
            { "user_id": user_id, "video_id": video_id }
        )
        self.video_col.update(
            { "video_id": video_id },
            { "$inc": { "like": -1} }
        )

    def query_like_info(self, user_id, video_id):
        return (self.video_like_col.find_one(
            { "user_id": user_id, "video_id": video_id }
        ) is not None)

    def query_like_info_by_user(self, user_id):
        return self.video_like_col.find(
            { "user_id": user_id }
        )

    def query_like_info_by_video(self, video_id):
        return self.video_like_col.find(
            { "video_id": video_id }
        )

    def count_like_info_by_user(self, user_id):
        return self.video_like_col.find(
            { "user_id": user_id }
        ).count()

    def count_like_info_by_video(self, video_id):
        return self.video_like_col.find(
            { "video_id": video_id }
        ).count()

    # ABOUT COMMENT

    def assign_comment_floor(self, video_id):
        tmp = self.comment_floor_ctrl_col.find_and_modify(
            query = { "video_id": video_id },
            update = { "$inc": { "floor_cnt": 1 } },
            new = True,
            upsert = True
        )
        return int(tmp["floor_cnt"])

    def insert_comment(self, comment):
        self.comment_col.insert(comment)

    def get_comment_by_comment_id(self, comment_id):
        return self.comment_col.find_one({ "comment_id": comment_id})

    def get_comment_by_video_id(self, video_id, offset, size):
        return self.comment_col.find({
            "$query": { "video_id": video_id },
            "$orderby": { "floor": 1 }
        })[offset : size]

    def get_comment_by_user_id(self, user_id, offset, size, reverse):
        return self.comment_col.find({
            "$query": { "user_id": user_id },
            "$orderby": { "reply_time": -1 if reverse else 1 }
        })[offset : size]

    def remove_comment_by_id(self, comment_id):
        d = self.comment_col.find({ "comment_id": comment_id })
        for each in d:
            each.pop("_id")
            self.comment_trash_col.insert(each)
        d = self.comment_col.find_and_modify(
            query = { "comment_id": comment_id },
            remove = True
        )

    # about comment

    def insert_barrage(self, barrage_dict):
        self.barrage_col.insert(barrage_dict)

    def get_barrage_by_video(self, video_id):
        return self.barrage_col.find({ "video_id": video_id })


