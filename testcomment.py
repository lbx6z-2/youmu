__author__ = 'badpoet'

import unittest
import youmu
import json

class CommentTestCase(unittest.TestCase):

    def setUp(self):
        self.app = youmu.create_app().test_client()

    def test_post_comment_without_login(self):
        #  not login
        rv = self.app.post("/api/comment/video/1", data = json.dumps(dict(
            content = "unit test"
        ), ensure_ascii = False))
        assert json.loads(rv.data)["state"] == "need login"

    def test_post_empty_comment(self):
        self.app.post("/api/user/_login", data = json.dumps(dict(
            username = "zxk12",
            password = "SRMYUEME555"
        )))
        rv = self.app.post("/api/comment/video/1", data = json.dumps(dict(
            content = ""
        ), ensure_ascii = False))
        assert json.loads(rv.data)["state"] == "empty content"

    def stage_post_comment_1_post(self):
        self.app.post("/api/user/_login", data = json.dumps(dict(
            username = "zxk12",
            password = "SRMYUEME555"
        )))
        return self.app.post("/api/comment/video/1", data = json.dumps(dict(
            content = "unit test code: abc6174xyz"
        ), ensure_ascii = False))

    def stage_post_comment_2_check_video(self):
        return self.app.get("/api/comment/video/1")

    def stage_post_comment_3_check_user(self):
        return self.app.get("/api/comment/user/zxk12")

    def stage_post_comment_4_delete(self):
        rv = self.app.get("/api/comment/video/1")
        comments = json.loads(rv.data)
        cid = ""
        for each in comments:
            if each["content"].find("abc6174xyz") >= 0:
                cid = each["comment_id"]
        assert len(cid) > 0
        self.app.delete("/api/comment/" + cid)
        return self.app.get("/api/comment/user/zxk12")

    def test_post_comment(self):
        rv = self.stage_post_comment_1_post()
        assert json.loads(rv.data)["state"] == "ok"
        self.stage_post_comment_4_delete()

    def test_get_video_comments(self):
        self.stage_post_comment_1_post()
        rv = self.stage_post_comment_2_check_video()
        assert rv.data.find("abc6174xyz") >= 0
        self.stage_post_comment_4_delete()

    def test_get_user_comments(self):
        self.stage_post_comment_1_post()
        rv = self.stage_post_comment_3_check_user()
        assert rv.data.find("abc6174xyz") >= 0
        self.stage_post_comment_4_delete()

    def test_delete_by_owner(self):
        rv = self.stage_post_comment_1_post()
        rv = self.stage_post_comment_4_delete()
        assert rv.data.find("abc6174xyz") < 0

    def test_delete_by_admin(self):
        self.app.post("/api/user/_login", data = json.dumps(dict(
            username = "hwr12",
            password = "95259378hewr"
        )))
        self.app.post("/api/comment/video/1", data = json.dumps(dict(
            content = "unit test code: 87878787"
        )))
        self.app.post("/api/user/_login", data = json.dumps(dict(
            username = "zxk12",
            password = "SRMYUEME555"
        )))
        rv = self.app.get("/api/comment/video/1")
        comments = json.loads(rv.data)
        cid = ""
        for each in comments:
            if each["content"].find("87878787") >= 0:
                cid = each["comment_id"]
        assert len(cid) > 0
        rv = self.app.delete("/api/comment/" + cid)
        assert json.loads(rv.data)["state"] == "failed"
        self.app.get("/api/user/_transform")
        rv = self.app.delete("/api/comment/" + cid)
        assert json.loads(rv.data)["state"] == "ok"
        rv = self.app.get("/api/comment/video/1")
        assert rv.data.find("87878787") < 0
        self.app.get("/api/user/_transform")

if __name__ == "__main__":
    unittest.main()