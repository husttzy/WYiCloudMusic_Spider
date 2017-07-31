# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentItem(scrapy.Item):
	music_id = scrapy.Field()
	user_id = scrapy.Field()
	user_name = scrapy.Field()
	content = scrapy.Field()
	up_count = scrapy.Field()    
	

class MusicItem(scrapy.Item):
	singer_id = scrapy.Field()
	name = scrapy.Field()
	music_id = scrapy.Field()
	url = scrapy.Field()
	comment_count = scrapy.Field()

class WyiItem(scrapy.Item):
    # define the fields for your item here like:
	singer = scrapy.Field()
	singer_id = scrapy.Field()
	main_url = scrapy.Field()
	category = scrapy.Field()




