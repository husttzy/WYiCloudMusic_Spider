import re
import scrapy
import json
import requests
from bs4 import BeautifulSoup
from scrapy.http import Request
from wyi.items import WyiItem,MusicItem, CommentItem

class wyiSpider(scrapy.Spider):
	name = 'wyi_music'
	allow_domains = "music.163.com"
	base_url = "http://music.163.com"
	user_agent = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"
	headers = {'User-Agent': user_agent, 'Referer': 'http://music.163.com/','Cookie': 'appver=1.5.0.75771;MUSIC_U=e954e2600e0c1ecfadbd06b365a3950f2fbcf4e9ffcf7e2733a8dda4202263671b4513c5c9ddb66f1b44c7a29488a6fff4ade6dff45127b3e9fc49f25c8de500d8f960110ee0022abf122d59fa1ed6a2;',}

	def start_requests(self):
		artists_url = self.base_url + '/discover/artist'
		yield Request(artists_url, self.parse)

	def parse(self, response):
		divs = BeautifulSoup(response.text, 'lxml').find_all('div', class_='blk')
		cat_urls = []
		for div in divs:
			lists = div.find_all('a', class_='cat-flag')
			for a in lists:
				url = self.base_url+a['href']
				cat_urls.append(url)
		for url in cat_urls:
			yield Request(url, callback=self.get_artist_urls, meta={'url':url})
	
	#获取该分类的歌手url
	def get_artist_urls(self, response):
		for i in range(65, 91):
			url = str(response.meta['url'])+'&initial='
			url=url+str(i)
			yield Request(url, callback=self.get_artists)

	#获取分类下所有歌手的url
	def get_artists(self, response):
		singer_urls = BeautifulSoup(response.text, 'lxml').find('div', class_='m-sgerlist')
		if singer_urls is None:
			return
		else:
			singer_urls = singer_urls.find_all('a', class_='f-thide')
		cat_name = BeautifulSoup(response.text, 'lxml').find('div', id='singer-cat-nav').find('a', class_='z-slt').get_text()
		for a in singer_urls:
			url = self.base_url+a['href']
			singer_name = a.get_text()
			item = WyiItem()
			item['main_url'] = url
			item['category'] = cat_name
			item['singer'] = singer_name
			singer_id = url.split('=')[1]
			item['singer_id'] = singer_id
			yield item
			yield Request(url, callback=self.get_songs, meta={'singer_id':singer_id})

	#进入歌手的主页，获取该歌手热门歌曲的url
	def get_songs(self, response):
		singer_id = str(response.meta['singer_id'])
		musics = BeautifulSoup(response.text, 'lxml').find('div', id='song-list-pre-cache').find('ul', class_='f-hide')
		if musics is None:
			return
		else:
			musics = musics.find_all('a')
		for music in musics:
			music_item = MusicItem()
			music_item['singer_id']=singer_id
			url = self.base_url+music['href']
			music_item['url'] = url
			music_id = url.split('=')[1]
			music_item['music_id'] = music_id
			name = music.get_text()
			music_item['name']=name
			yield music_item
			yield Request(url, callback=self.get_commnets, meta={'music_id': music_id})

	#获取评论信息
	def get_commnets(self, response):
		music_id = str(response.meta['music_id'])
		url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s/?csrf_token=" % music_id
		data = {'params':'+jhuMCaBep4+4cSAkbzTb6JzWl7WxiQj5ntmf+lzmu7eWC/MA375uJHuUGHISZiAJy2QyS6HcxtTpHUSzm16UUuDnQglq9Ec7QKU9oDoOTLJR4eGjf+67A1+udOc9l5vrARCEkEGDLsgiHxmO9LNkyEbKa6HhExomAs9iFTImEXT/MBbvLdAGo1+8iB2TzdfF2M73ntlNuY+uX5dfVB4WIOtY9j8hAYIFM267mAQkYA=',
		'encSecKey':'333d4d0332f729bc3c32f3e6da6a8c607226047da91573d200430abdd909b5506d4cf2d9174c5fff5dd699ff7afdedc0a3ac0fbf269f9cfa2293eb29488188cbf6b9984bd725f188ac15a7f83de2194f56e3601d48995b0712450490b059dbb0f296f61243376466b95e0b5945fd102dfd3f4463c5db9c936600cf8f86e4526c'}
		response = requests.post(url, headers=self.headers, data=data)
		json_dict = json.loads(response.content.decode("utf-8"))
		json_comment = json_dict['comments']
		for json_comment in json_comment:
			comment = CommentItem()
			comment['music_id'] = music_id
			user_id = json_comment['user']['userId']
			comment['user_id'] = user_id
			user_name = json_comment['user']['nickname']
			comment['user_name'] = user_name
			comment['content'] = json_comment['content']
			comment['up_count'] = json_comment['likedCount']
			yield comment	
			
		  	
