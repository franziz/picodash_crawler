global MOCK_INPUT
MOCK_INPUT = {
	     "name":" autogenPointII 1",
	      "lat":"14.6526527",
	     "long":"120.881398",
	 "category":"blanketCover",
	    "track":"MakatiBlanket",
	     "city":"Makati",
	  "country":"Philippines",
	"processed":"FALSE",
	  "address":""
}

from lib.location_data import LocationData
from lib.picodash      import Picodash
from selenium          import webdriver
import selenium
import copy
import bson.json_util
import multiprocessing

def callback(media=None):
	assert media is not None, "media is not defined."
	print(bson.json_util.dumps(media, indent=4, separators=(",",":")))
#end def

def execute_thread(location_data=None, cookies=None):	
	assert cookies       is not None, "cookies is not defined."
	assert location_data is not None, "location_data is not defined."

	print("[picodash_crawler] Engine start!")

	picodash         = Picodash()
	picodash.cookies = cookies
	picodash.apply_cookies()
	picodash.crawl(location_data=location_data, callback=callback)

try:
	picodash = Picodash()
	picodash.login()

	# location_data = LocationData()
	# locations     = location_data.get_locations()
	locations     = [MOCK_INPUT for a in range(2)]

	for location in locations:
		procs = list()
		for a in range(1):
			p = multiprocessing.Process(
				target = execute_thread,
				  args = (location, picodash.cookies)
			)
			procs.append(p)
			p.start()

		for p in procs:
			p.join()
	
except selenium.common.exceptions.TimeoutException:
	picodash.driver.save_screenshot("./error.png")
	# instance.driver.save_screenshot("./picodash.png")
except:
	raise
