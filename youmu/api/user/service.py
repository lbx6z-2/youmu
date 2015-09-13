__author__ = 'badpoet'

import re

from youmu.clients import mongo
from youmu.models.user import User
from youmu.clients.tunetclient import tunet_login

class UserService(object):

    @staticmethod
    def mto(temp):
        return User(
            id = temp.get("id"),
            mid = str(temp.get("_id")),
            name = temp.get("name"),
            avatar = temp.get("avatar"),
            disabled = temp.get("disabled")
        )

    @staticmethod
    def is_valid_id(id):
        try:
            id = str(id)
            return re.match(r'[0-9a-zA-Z\_\-]{1,15}', id) != None
        except Exception, e:
            print e
            return False

    @staticmethod
    def load_user_by_id(id):
        temp = mongo.get_user_by_id(id)
        if not temp:
            return None
        obj = UserService.mto(temp)
        return obj

    @staticmethod
    def create_user(id, name, avatar, disabled):
        if mongo.has_user_id(id):
            return None
        mongo.insert_user({
            "id": id,
            "name": name,
            "avatar": avatar,
            "disabled": False
        })

    @staticmethod
    def authenticate(id, password):
        # print id, UserService.is_valid_id(id)
        # print password, UserService.is_valid_password(password)
        if not UserService.is_valid_id(id):
            return None
        tunet_user = tunet_login(id, password)
        if tunet_user is None:
            return None
        if not mongo.has_user_id(tunet_user["id"]):
            UserService.create_user(
                id = tunet_user["id"],
                name = tunet_user["name"],
                avatar = "",
                disabled = False
            )
        user = UserService.load_user_by_id(tunet_user["id"])
        return user

    @staticmethod
    def update(user_id, name, avatar):
        if not user_id:
            return "need login"
        if not mongo.has_user_id(user_id):
            return "no such person"
        data = mongo.get_user_by_id(user_id)
        if name:
            data["name"] = name
        if avatar:
            data["avatar"] = avatar
        mongo.update_user(data)
        return "ok"

    @staticmethod
    def disable(user_id, state = True):
        if not user_id:
            return False
        if not mongo.has_user_id(user_id):
            return False
        mongo.disable_user(user_id, state)
        return True

    @staticmethod
    def transform_admin(user_id):
        mongo.transform_admin(user_id)

    @staticmethod
    def list_users(offset, size):
        return {
            "total": mongo.count_users(),
            "result": [UserService.mto(u) for u in mongo.list_users(offset, size)]
        }

    @staticmethod
    def get_user_by_name(user_name):
        return UserService.mto(mongo.get_user_by_name(user_name))
