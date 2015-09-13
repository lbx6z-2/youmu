__author__ = 'badpoet'

from youmu.clients import mongo
from youmu.models.barrage import Barrage
from youmu.api.video.service import VideoService
from youmu.models.video import Video

class BarrageService(object):

    @staticmethod
    def mto(item):
        return Barrage(
            item.get("video_id"),
            item.get("user_id"),
            item.get("content"),
            item.get("position"),
            item.get("mode"),
            item.get("size"),
            item.get("color"),
            item.get("pool"),
            item.get("stamp")
        )

    @staticmethod
    def add_barrage(barrage):
        if VideoService.get_media_type_by_id(barrage.video_id) == Video.LIVE:
            return
        mongo.insert_barrage(barrage.to_dict())

    @staticmethod
    def get_barrage_on_video(video_id):
        cursor = mongo.get_barrage_by_video(video_id)
        res = [BarrageService.mto(e) for e in cursor]
        return res

    @staticmethod
    def obj_list_to_xml(b_list):
        temp = u'''<?xml version="1.0" encoding="UTF-8"?>
	        <i>
		        <chatserver>youmu</chatserver>
		        <chatid>1</chatid>
		        <mission>0</mission>
		        <source>k-v</source>
	        '''
        for e in b_list:
            temp += unicode(e.to_xml())
        temp += "</i>"
        return temp