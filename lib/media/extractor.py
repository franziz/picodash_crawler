from .. import tools
import selenium
import time
import random

class MediaExtractor(object):
	def __init__(self, webdriver=None):
		self.driver = webdriver

	def extract(self):
		""" This function has to be success.
		    If something happes with this function, you need to try again again and again
		"""
		success = False
		while not success:
			try:
				assert self.driver is not None, "driver is not defined."
				print("[igfollowers] Getting media")
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
				media = self.driver.find_element_by_xpath("//div[@id='media']")
				media = media.find_elements_by_class_name("grid-cell")
				success = True
			except exceptions.MaxTryExceeded:
				# this will fail if MediaExtractor cannot find element
				# I assume that this is because of running out of API request
				# API hit the limit
				print("[picodash_crawler] Media cannot be loaded.")
				time_to_wait = random.randint(300,600)
				tools._wait(duration=time_to_wait)	
		return media