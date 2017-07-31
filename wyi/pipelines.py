# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import datetime
from scrapy import log
from .items import CommentItem, MusicItem, WyiItem

class WyiPipeline(object):
	def __init__(self):
		Client = MongoClient(host="127.0.0.1",port=27017)
		print("mongodb")
		db = Client['wyi_muscic']
		self.singer = db['singer']
		self.music = db['music']
		self.comment = db['comment']
	def process_item(self, item, spider):
		if isinstance(item, WyiItem):
			try:
				self.singer.insert(dict(item))
			except Exception:
				pass
		if isinstance(item, MusicItem):
			try:
				self.music.insert(dict(item))
			except Exception:
				pass
		if isinstance(item, CommentItem):
			try:
                                self.comment.insert(dict(item))
			except Exception:
				pass
		log.msg('item added to mongodb database!',  
              level=log.DEBUG,spider=spider) 
		return item
