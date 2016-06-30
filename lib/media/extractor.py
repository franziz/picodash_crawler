import selenium
import time
import random

class MediaExtractor(object):
	def __init__(self, webdriver=None):
		self.driver = webdriver

	def extract(self):
		assert self.driver is not None, "driver is not defined."

		max_tried = 10
		tried     = 0
		loaded    = False
		while not loaded:
			try:
				self.driver.find_element_by_xpath("//div[@id='media']")
				time.sleep(random.randint(1000,3000)/1000)
				loaded = True
			except selenium.common.exceptions.NoSuchElementException:
				tried = tried + 1

		if tried >= max_tried: raise exceptions.MaxTryExceeded("Max try exceeded while trying to get media.")

		time.sleep(random.randint(100,5000)/1000)
		media = self.driver.find_element_by_xpath("//div[@id='media']")
		media = media.find_elements_by_class_name("grid-cell")
		
		return media