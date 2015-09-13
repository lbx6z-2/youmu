# -*- coding=utf-8 -*-

__author__ = 'badpoet'

import unittest
import youmu
import json

class AnonymousUserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = youmu.create_app().test_client()

    def tearDown(self):
        pass

    def test_tell(self):
        rv = self.app.get('/api/user/_tell')
        assert rv.data == "You are a tourist."

    def test_login(self):
        rv = self.app.post('/api/user/_login', data = json.dumps(dict(
            username = "zxk12",
            password = "SRMYUEME555"
        )))
        assert json.loads(rv.data)["state"] == "ok"

    def test_logout(self):
        rv = self.app.post('/api/user/_logout')
        assert json.loads(rv.data)["state"] == "ok"

    def test_incorrectly_login(self):
        rv = self.app.post('/api/user/_login', data = json.dumps(dict(
            username = "fake",
            password = "incorrect"
        )))
        assert json.loads(rv.data)["state"] == "failed"

    def test_get_me(self):
        rv = self.app.get('/api/user/_me')
        assert rv.data == ""

    def test_update_me(self):
        rv = self.app.put("/api/user/_me")
        assert rv.data == ""

    def test_disable_user(self):
        rv = self.app.post("/api/user/zxk12/_disable")
        assert json.loads(rv.data)["state"] == "need admin"

    def test_enable_user(self):
        rv = self.app.post("/api/user/zxk12/_enable")
        assert json.loads(rv.data)["state"] == "need admin"

    def test_list_users(self):
        rv = self.app.get("/api/user/")
        assert json.loads(rv.data)["state"] == "need admin"

    def test_transform(self):
        rv = self.app.get("/api/user/_transform")
        assert rv.data == "failed"

    def test_get_user(self):
        rv = self.app.get("/api/user/zxk12")
        assert json.loads(rv.data)["state"] == "need admin"

class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = youmu.create_app().test_client()
        rv = self.app.post('/api/user/_login', data = json.dumps(dict(
            username = "zxk12",
            password = "SRMYUEME555"
        )))

    def tearDown(self):
        self.app.post('/api/user/_logout')

    def test_tell(self):
        rv = self.app.get("/api/user/_tell")
        assert rv.data == (u"You are 张洵恺").encode("utf-8")

    def test_transform(self):
        rv = self.app.get("/api/user/_transform")
        assert rv.data == "transformed"
        rv = self.app.get("/api/user/_transform")
        assert rv.data == "transformed"

    def test_get_me(self):
        rv = self.app.get("/api/user/_me")
        me = json.loads(rv.data)
        assert me["id"] == "zxk12"
        assert me["name"] == u"张洵恺"

    def test_put_me(self):
        rv = self.app.put("/api/user/_me", data = dict(
            name = "hi",
            avatar = file("/Users/badpoet/Maskball/orange.jpg")
        ), content_type = "multipart/form-data")
        assert json.loads(rv.data)["state"] == "ok"
        assert json.loads(self.app.get("/api/user/_me").data)["name"] == "hi"
        rv = self.app.put("/api/user/_me", data = dict(
            name = u"张洵恺",
            avatar = file("/Users/badpoet/Maskball/orange.jpg")
        ), content_type = "multipart/form-data")

    def test_disable_user(self):
        rv = self.app.post("/api/user/zxk12/_disable")
        assert json.loads(rv.data)["state"] == "need admin"

    def test_enable_user(self):
        rv = self.app.post("/api/user/zxk12/_enable")
        assert json.loads(rv.data)["state"] == "need admin"

    def test_list_users(self):
        rv = self.app.get("/api/user/")
        assert json.loads(rv.data)["state"] == "need admin"

    def test_get_user(self):
        rv = self.app.get("/api/user/zxk12")
        assert json.loads(rv.data)["state"] == "need admin"

class AdminUserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = youmu.create_app().test_client()
        self.app.post('/api/user/_login', data = json.dumps(dict(
            username = "zxk12",
            password = "SRMYUEME555"
        )))
        self.app.get("/api/user/_transform")

    def tearDown(self):
        self.app.get("/api/user/_transform")
        self.app.post("/api/user/_logout")

    def test_disable_user(self):
        rv = self.app.post("/api/user/zxk12/_disable")
        assert json.loads(rv.data)["state"] == "ok"
        rv = self.app.get("/api/user/zxk12")
        assert json.loads(rv.data)["disabled"] == True

    def test_enable_user(self):
        rv = self.app.post("/api/user/zxk12/_enable")
        assert json.loads(rv.data)["state"] == "ok"
        rv = self.app.get("/api/user/zxk12")
        assert json.loads(rv.data)["disabled"] == False

    def test_list_users(self):
        rv = self.app.get("/api/user/")
        assert len(json.loads(rv.data)["result"]) > 0

    def test_get_users(self):
        rv = self.app.get("/api/user/zxk12")
        assert json.loads(rv.data)["name"] == u"张洵恺"

if __name__ == "__main__":
    unittest.main()