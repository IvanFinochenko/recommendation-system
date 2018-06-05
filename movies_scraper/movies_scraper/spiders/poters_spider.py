import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from movies_scraper.items import Rating, Movie, MoviesGenre, MoviesAward, Poster
import pandas as pd
import hashlib
import re
from movies_scraper.settings import DATABASE
import psycopg2 as pg

class MoviesSpider(CrawlSpider):
	name = 'posters_spider'
	allowed_domains = ['www.kinopoisk.ru']
	start_urls=['https://www.kinopoisk.ru/action/connoisseur/']

	def start_requests(self):
		connection = pg.connect(user=DATABASE['username'], password=DATABASE['password'], dbname=DATABASE['database'])
		self.moviesId = pd.read_sql('select movie_id from movies where poster is null', connection)['movie_id'].tolist()
		for movie_id in self.moviesId:
			yield scrapy.Request(
				'https://www.kinopoisk.ru/film/' + str(movie_id),
				callback=self.parse_poster, 
				meta={'movie_id': movie_id})

	def parse_poster(self, response):
		poster_url = response.selector.xpath('.//div[contains(@class, "film-img-box")]').xpath('.//img/@src').extract_first()
		poster = Poster()
		poster['movie_id'] = response.meta.get('movie_id')
		poster['poster_url'] = poster_url
		yield poster

