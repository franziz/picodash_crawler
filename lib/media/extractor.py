from ..      import tools, exceptions
from pymongo import MongoClient
import selenium
import time
import random
import copy

class MediaExtractor(object):
	def __init__(self, webdriver=None):
		self.driver = webdriver
		self.db     = MongoClient("mongodb://hotp:hotp7890@220.100.163.134:27017/test?authSource=hotp")
		self.db  	= self.db.hotp

	def extract(self):
		""" This function has to be success.
		    If something happes with this function, you need to try again again and again
		"""
		success = False
		while not success:
			try:
				assert self.driver is not None, "driver is not defined."
				print("[picodash_crawler] Getting media")
				max_tried = 10
				tried     = 0
				loaded    = False
				while not loaded:
					try:
						time.sleep(random.randint(1000,3000)/1000)
						self.driver.find_element_by_xpath("//div[@id='media']")
						loaded = True
					except selenium.common.exceptions.NoSuchElementException:
						tried = tried + 1

				if tried >= max_tried: raise exceptions.MaxTryExceeded("Max try exceeded while trying to get media.")

				time.sleep(random.randint(100,5000)/1000)
				all_media = self.driver.find_element_by_xpath("//div[@id='media']")
				all_media = all_media.find_elements_by_class_name("grid-cell")

				# This function will check if the post_url has been inserted into database.
				# The function will help to reduce total number of request.
				media     = []
				for medium in all_media:
					post_url = medium.find_element_by_xpath("./div[@class='moreInfo']/a")
					post_url = post_url.get_attribute("href")
					duplicate = True if self.db.hotp_geoposts.count({"PostUrl":post_url}) > 0 else False
					if not duplicate:
						media.append(copy.copy(medium))
				success = True
			except exceptions.MaxTryExceeded:
				# this will fail if MediaExtractor cannot find element
				# I assume that this is because of running out of API request
				# API hit the limit
				print("[picodash_crawler] Media cannot be loaded.")
				time_to_wait = random.randint(300,600)
				tools._wait(duration=time_to_wait)	
		return media