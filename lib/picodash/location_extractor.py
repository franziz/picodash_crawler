from .. import exceptions
import selenium
import time
import random

class LocationExtractor():
	def __init__(self, webdriver=None):
		assert webdriver is not None, "webdriver is not defined."
		self.driver = webdriver

	def extract(self, lat=None, long=None):
		assert lat         is not None, "lat is not defined."
		assert long        is not None, "long is not defined."
		assert self.driver is not None, "webdriver is not defined."

		print("[picodash_crawler] Location: {},{}".format(lat, long))
		location_url = "https://www.picodash.com/explore/locations?location={lat}%20{long}".format(
							 lat = lat,
							long = long
						)
		self.driver.get(location_url)

		# Wait until element loaded
		max_tried = 10
		tried     = 0
		loaded    = False
		while not loaded and tried < max_tried:
			try:
				self.driver.find_element_by_xpath("//div[@class='grid-cell']")
				time.sleep(random.randint(1000,3000)/1000)
				loaded = True
			except selenium.common.exceptions.NoSuchElementException:
				tried = tried + 1

		if tried >= max_tried: raise exceptions.MaxTryExceeded("Max try exceeded while trying to get location on grid-cell")
		
		time.sleep(random.randint(100,5000)/1000)
		location_components = self.driver.find_elements_by_xpath("//div[@class='grid-cell']")
		locations           = list()
		del location_components[0]
		for location in location_components:
			location_name = location.text
			location_name = location_name.replace("\n","")
			location_link = location.find_element_by_xpath(".//a")
			location_link = location_link.get_attribute("href")
			if "locations/0" not in location_link:
				locations.append({
					"name" : location_name,
					"link" : location_link	
				})

		return locations
	#end def
#end class