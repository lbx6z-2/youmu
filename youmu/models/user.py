__author__ = 'badpoet'

import json
from youmu.clients import mongo

class User(object):

    def __init__(self, id = "", mid = "", name = "", avatar = "", password = "", disabled = False):
        self.id = id
        self.mid = mid
        self.name = name
        self.avatar = avatar if len(avatar) > 0 else "/static/img/human-head-with-question-mark.jpg"
        self.disabled = disabled

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def check_password(self):
        return self.password == password

    def is_admin(self):
        return mongo.check_admin(self.id)

    def to_dict(self):
        dic = {
            "id": self.id,
            "name": self.name,
            "avatar": self.avatar,
            "admin": self.is_admin(),
            "disabled": self.disabled
        }
        return dic
