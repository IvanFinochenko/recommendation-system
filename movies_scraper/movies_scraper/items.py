# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Rating(scrapy.Item):
	user_id = scrapy.Field()
	movie_id = scrapy.Field()
	vote = scrapy.Field()

class Movie(scrapy.Item):
	movie_id = scrapy.Field()
	title = scrapy.Field()
	year = scrapy.Field()
	country = scrapy.Field()
	director = scrapy.Field()
	rating = scrapy.Field()
	runtime = scrapy.Field()
	count_reviews = scrapy.Field()
	percent_good_reviews = scrapy.Field()
	critics_rating = scrapy.Field()
	critics_rating_russian = scrapy.Field()
	budget = scrapy.Field()
	box_office = scrapy.Field()
	age = scrapy.Field()
	image = scrapy.Field()

class MoviesGenre(scrapy.Item):
	movie_id = scrapy.Field()
	genre_id = scrapy.Field()

class MoviesAward(scrapy.Item):
	movie_id = scrapy.Field()
	award_id = scrapy.Field()
	count_wins = scrapy.Field()
	count_nominations = scrapy.Field()

class Genre(scrapy.Item):
	genre_id = scrapy.Field()
	genre_name = scrapy.Field()

class Award(scrapy.Item):
	award_id = scrapy.Field()
	award_name = scrapy.Field()

class Poster(scrapy.Item):
	movie_id = scrapy.Field()
	poster_url = scrapy.Field()