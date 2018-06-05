import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
#from movies_scraper.items import Rating, Movie, MoviesGenre, MoviesAward
import pandas as pd
import hashlib
import re
from movies_scraper.settings import DATABASE
import psycopg2 as pg

class MoviesSpider(CrawlSpider):
	name = 'movies_spider'
	allowed_domains = ['www.kinopoisk.ru']
	start_urls=['https://www.kinopoisk.ru/action/connoisseur/']

	# def parse(self, response):
	# 	table_info = response.selector.xpath('//table[contains(@class, "info")]')
	# 	runtime = re.search(r'\d+', table_info.xpath('.//td[@id="runtime"]/text()').extract_first())
	# 	print(runtime)

	
	def start_requests(self):
		connection = pg.connect(user=DATABASE['username'], password=DATABASE['password'], dbname=DATABASE['database'])
		self.genre_movies_id = pd.read_sql('select distinct movie_id from movies_genre', connection)['movie_id'].tolist()
		self.users_id = pd.read_sql('select distinct user_id from ratings', connection)['user_id'].tolist()
		self.moviesId = pd.read_sql('select movie_id from movies', connection)['movie_id'].tolist()
		self.dim_genres = pd.read_sql('select genre_name, genre_id from genres', connection)
		self.dim_awards = pd.read_sql('select * from awards', connection)
		self.dim_awards = dict(zip(self.dim_awards['award_name'],self.dim_awards['award_id']))
		self.dim_genres = dict(zip(self.dim_genres['genre_name'],self.dim_genres['genre_id']))
		yield scrapy.Request('https://www.kinopoisk.ru/action/connoisseur', callback = self.parse_users_list)

	def parse_users_list(self, response):
		print('parse_users_list')
		for user in response.selector.xpath('//a[@target="_blank"]'):
			user_id = user.xpath('./@href').extract_first()
			yield scrapy.Request(user_id + '/votes/list/ord/date/genre/films/vs/vote/page/1/#list',
								callback = self.parse_user_votes,
								meta = {'page': 1})
			print(user_id)

	def parse_user_votes(self, response):
		print('parse_user_votes')
		for item in response.css('.item'):
			movie_name = item.xpath('.//div[@class="nameRus"]/a/text()').extract_first()
			movie_url = item.xpath('.//div[@class="nameRus"]/a/@href').extract_first()
			vote = item.xpath('.//div[@class="vote"]/text()').extract_first()
			if movie_name and vote:
				user_id = re.search(r'\d+', response.request.url).group(0)
				movie_id = int(re.findall(r'\d+', movie_url)[-1])
				rating = Rating()
				rating['user_id'] = user_id
				rating['movie_id'] = movie_id
				rating['vote'] = vote
				#yield rating
				# if movie_id not in self.moviesId:
				# 	self.moviesId.append(movie_id)
				# 	yield scrapy.Request('https://www.kinopoisk.ru' + movie_url, 
				# 						callback = self.parse_movie, 
				# 						meta = {'movie_id': movie_id})
				if movie_id in self.moviesId:
					if user_id not in self.users_id and movie_id not in self.genre_movies_id:
						self.users_id.append(user_id)
						yield rating
					if movie_id not in self.genre_movies_id:
						self.genre_movies_id.append(movie_id)
						yield scrapy.Request('https://www.kinopoisk.ru' + movie_url, 
											callback = self.parse_movie, 
											meta = {'movie_id': movie_id})
		page_num = int(response.meta.get('page')) + 1
		page = 'page/{}'.format(page_num)
		yield scrapy.Request(re.sub(r'page/\d+', page, response.request.url), 
							callback = self.parse_user_votes,
							meta = {'page': page_num})

	def parse_movie(self, response):
		print('parse_movie')
		movie_id = response.meta.get('movie_id')
		table_info = response.selector.xpath('//table[contains(@class, "info")	]')
		title = response.selector.xpath('//h1[@class="moviename-big"]/text()').extract_first()
		year = table_info.xpath('.//td[text()="год"]/../td/div/a/text()').extract_first()
		country = table_info.xpath('.//td[text()="страна"]/../td/div/a/text()').extract_first()
		director = table_info.xpath('.//td[text()="режиссер"]/../td/a/text()').extract_first()
		rating = response.selector.xpath('//span[@class="rating_ball"]/text()').extract_first()
		runtime = re.search(r'\d+', table_info.xpath('.//td[@id="runtime"]/text()').extract_first())
		genres = []
		for item in table_info.xpath('.//span[@itemprop="genre"]/a'):
			genres.append(item.xpath('.//text()').extract_first())
		count_reviews = response.selector.xpath('//li[@class="all"]/b/text()').extract_first()
		percent_good_reviews = response.selector.xpath('//li[@class="perc"]/b/text()').extract_first()
		critics_rating = response.selector.xpath('//div[@class="criticsRating criticsRatingDouble"]/div/div[@class="ratingNum"]/span/text()').extract_first()
		critics_rating_russian = response.selector.xpath('//a[@class="ratingNum ratingNumLink"]/span/text()').extract_first()
		if not critics_rating:
			critics_rating = response.selector.xpath('//div[@class="criticsRating"]/div[@class="ratingNum"]/span/text()').extract_first()
		age = -1
		age_tag = table_info.xpath('.//td/div[contains(@class, "ageLimit")]/@class').extract_first()
		if age_tag:
			age = re.findall(r'\d+', age_tag)[-1]
		if year and runtime and percent_good_reviews:
			runtime = runtime.group(0)
			movie = Movie()
			movie['movie_id'] = movie_id
			movie['title'] = title
			movie['year'] = year
			movie['country'] = country
			movie['director'] = director
			movie['rating'] = rating
			movie['runtime'] = runtime
			movie['count_reviews'] = count_reviews
			movie['percent_good_reviews'] = percent_good_reviews[:-1]
			movie['critics_rating'] = critics_rating
			movie['critics_rating_russian'] = critics_rating_russian
			movie['age'] = age
			movies_genre = MoviesGenre()
			for genre in genres:
				movies_genre['movie_id'] = movie_id
				movies_genre['genre_id'] = self.dim_genres[genre]
				yield movies_genre
			yield scrapy.Request(
				response.request.url + '/box', 
				callback = self.parse_box_office,
				meta = {'movie': movie, 'handle_httpstatus_list': [404]})

	def parse_box_office(self, response):
		print('parse_box_office')
		movie = response.meta.get('movie')
		budget = 0
		box_office = 0
		if response.status == 404:
			print('404')
		else:
			box_office_text = re.search(
				r'\d+',
				response.selector.xpath('//td/b[text()="Общие сборы:"]/../../following-sibling::tr[1]/td/h3/font/text()').extract_first().replace(u'\xa0', ''))
			if box_office_text:
				box_office = box_office_text.group(0)
			budget_text = re.search(
				r'\d+',
				response.selector.xpath('//td/b[text()="Итого:"]/../../following-sibling::tr[1]/td/h3/font/text()').extract_first().replace(u'\xa0', ''))
			if budget_text:
				budget = budget_text.group(0)
		movie['budget'] = budget
		movie['box_office'] = box_office
		# yield scrapy.Request(
		# 	response.request.url[:-4] + '/studio',
		# 	callback = self.parse_studio,
		# 	meta = {'movie': movie})
		yield scrapy.Request(
			response.request.url[:-4] + '/awards', 
			callback = self.parse_awards,
			meta = {'movie_id': movie['movie_id'], 'handle_httpstatus_list': [404]})

	def parse_awards(self, response):
		print('parse_awards')
		movie_id = response.meta.get('movie_id')
		if response.status == 404:
			print('404')
		else:
			awards = {}
			for award in response.selector.xpath('//td/b/a'):
				wins = 0
				nominations = 0
				wins_text = award.xpath('.//../../../following-sibling::tr/td/font/b[text()="Победитель"]/../../text()').extract_first()
				if wins_text:
					wins = re.search(r'\d+', wins_text).group(0)
				nominations_text = award.xpath('.//../../../following-sibling::tr/td/b[text()="Номинации"]/../text()').extract_first()
				if nominations_text:
					nominations = re.search(r'\d+', nominations_text).group(0)
				award = award.xpath('.//text()').extract_first()
				award = award[:award.find(',')]
				award_id = self.dim_awards[award]
				movies_award = MoviesAward()
				movies_award['movie_id'] = movie_id
				movies_award['award_id'] = award_id
				movies_award['count_wins'] = int(wins)
				movies_award['count_nominations'] = int(nominations)
				if award_id in awards:
					movies_award['count_wins'] = movies_award['count_wins'] + awards[award_id]['count_wins']
					movies_award['count_nominations'] = movies_award['count_nominations'] + awards[award_id]['count_nominations']
				awards[award_id] = movies_award	
			for key, value in awards.items():
				yield value

	def parse_studio(self, response):
		movie = response.meta.get('movie')
		image = -1
		image_tag = response.selector.xpath('//td[text()="цветное"]').extract_first()
		if image_tag:
			image = 1
		else:
			image_tag = response.selector.xpath('//td[text()="чёрно-белое"]').extract_first()
			if image_tag:
				image = 0
		movie['image'] = image
		yield movie