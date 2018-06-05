# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
from movies_scraper.items import *
from movies_scraper.settings import DATABASE

class PostgresPipeline(object):
	def open_spider(self, spider):
		self.connection = psycopg2.connect(user=DATABASE['username'], password=DATABASE['password'], dbname=DATABASE['database'])
		self.cur = self.connection.cursor()

	def close_spider(self, spider):
		print('commit')
		#self.connection.commit()
		self.cur.close()
		self.connection.close()

	def process_item(self, item, spider):
		try:
			if type(item) is Genre:
				self.cur.execute(
					"insert into genres(genre_id, genre_name) values(%s,%s)",(item['genre_id'],item['genre_name']))
			if type(item) is Award:
				self.cur.execute(
					"insert into awards(award_id, award_name) values(%s,%s)",(item['award_id'],item['award_name']))
			if type(item) is Movie:
				insert = """insert into movies(
					 movie_id, 
					 title, 
					 year,
					 country,
					 director,
					 rating,
					 runtime,
					 count_reviews,
					 percent_good_reviews,
					 critics_rating,
					 critics_rating_russian, 
					 budget,
					 box_office,
					 age,
					 image)
					 values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
				print(insert)
				self.cur.execute(
					insert,
					(item['movie_id'],
					 item['title'],
					 item['year'],
					 item['country'],
					 item['director'],
					 item['rating'],
					 item['runtime'],
					 item['count_reviews'],
					 item['percent_good_reviews'],
					 item['critics_rating'],
					 item['critics_rating_russian'],
					 item['budget'],
					 item['box_office'],
					 item['age'],
					 item['image']))
			if type(item) is MoviesGenre:
				self.cur.execute(
					"insert into movies_genre(movie_id, genre_id) values(%s,%s)", (item['movie_id'], item['genre_id']))
			if type(item) is MoviesAward:
				self.cur.execute(
					"insert into movies_award(movie_id, award_id, count_wins, count_nominations) values(%s,%s,%s,%s)",
					(item['movie_id'],
					 item['award_id'],
					 item['count_wins'],
					 item['count_nominations']))
			if type(item) is Rating:
				self.cur.execute(
					"insert into ratings(user_id, movie_id, vote) values(%s,%s,%s)",
					(item['user_id'],
					 item['movie_id'],
					 item['vote']))
			self.connection.commit()
		except psycopg2.DatabaseError as e:
			print("Error: %s" % e)
		return item

class PosterPipeline(object):
	def open_spider(self, spider):
		self.connection = psycopg2.connect(user=DATABASE['username'], password=DATABASE['password'], dbname=DATABASE['database'])
		self.cur = self.connection.cursor()

	def close_spider(self, spider):
		print('commit')
		#self.connection.commit()
		self.cur.close()
		self.connection.close()

	def process_item(self, item, spider):
		try:
			self.cur.execute(
				'update movies set poster=%s where movie_id=%s', (item['poster_url'], item['movie_id']))
			self.connection.commit()
		except psycopg2.DatabaseError as e:
			print("Error: %s" % e)
		return item