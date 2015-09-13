__author__ = 'badpoet'

from datetime import datetime

class Barrage(object):

    def __init__(self, video_id, user_id, content, position, mode, size, color, pool, stamp):
        self.video_id = video_id
        self.user_id = user_id
        self.content = content
        self.position = position
        self.mode = mode
        self.size = size
        self.color = color
        self.pool = pool
        self.stamp = stamp

    def to_dict(self):
        return {
            "video_id": self.video_id,
            "user_id": self.user_id,
            "content": self.content,
            "position": self.position,
            "mode": self.mode,
            "size": self.size,
            "color": self.color,
            "pool": self.pool,
            "stamp": self.stamp
        }

    def to_xml(self):
        p = ",".join([
            str(self.position),
            str(self.mode),
            str(self.size),
            str(self.color),
            str((self.stamp - datetime(1970, 1, 1, 8)).total_seconds()),
            str(self.pool),
            str(self.user_id),
            str(0)  # TODO barrage row id (for barrage history)
        ])
        return '<d p="' + p + '">' + self.content + '</d>'

