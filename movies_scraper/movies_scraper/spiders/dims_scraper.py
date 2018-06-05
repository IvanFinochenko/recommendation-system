# import scrapy
# from scrapy.spiders import CrawlSpider
# from movies_scraper.items import Genre, Award
# import re

# class DimsScraper(CrawlSpider):
# 	name = 'dims_spider'
# 	allowed_domains = ['www.kinopoisk.ru']
# 	start_urls=['https://www.kinopoisk.ru/lists/m_act%5Bgenre%5D/1750/']

# 	def parse(self, response):
# 		genre_id = 1
# 		genre_tag = response.selector.xpath('//td/b')
# 		genre  = Genre()
# 		genre['genre_id'] = genre_id
# 		genre['genre_name'] = genre_tag.xpath('.//text()').extract_first()
# 		yield genre
# 		for item in response.selector.xpath('//td[@valign="top"]/a[@class="all"]'):
# 			genre_id += 1
# 			genre['genre_id'] = genre_id
# 			genre['genre_name'] = item.xpath('.//text()').extract_first()
# 			yield genre
# 		self.award_id = 1
# 		yield scrapy.Request('https://www.kinopoisk.ru/awards/', callback = self.parse_awards)

# 	def parse_awards(self, response):
# 		award = Award()
# 		for award_name in response.selector.xpath('//td/a[@class="continue"]/b/text()').extract():
# 			award['award_id'] = self.award_id
# 			award['award_name'] = award_name
# 			self.award_id += 1
# 			yield award


