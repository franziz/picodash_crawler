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
from lib.media_saver   import MediaSaver
from selenium          import webdriver
import selenium
import bson.json_util
import multiprocessing
import pymongo

def callback(media=None):
	assert media is not None, "media is not defined."
	try:
		media_saver = MediaSaver()
		media_saver.save(media)
		print("[picodash_crawler] Inserted one document!")
	except pymongo.errors.DuplicateKeyError:
		print("[picodash_crawler] Ops! Duplicate Data!")

	# print(bson.json_util.dumps(media, indent=4, separators=(",",":")))
#end def

def execute_thread(data=None):	
	assert data is not None, "data is not defined."

	location_data = data[0]
	cookies       = data[1]

	print("[picodash_crawler] Engine start!")

	picodash         = Picodash()
	picodash.cookies = cookies
	picodash.apply_cookies()
	picodash.crawl(location_data=location_data, callback=callback)

if __name__ == "__main__":
	try:
		picodash = Picodash()
		picodash.login()

		location_data = LocationData()
		locations     = location_data.get_locations()
		locations     = [(location, picodash.cookies) for location in locations]

		print("[picodash_crawler] Number of Locations: {}".format(len(locations)))

		multi_process = multiprocessing.Pool(10)
		multi_process.map(execute_thread, locations)		
		
	except selenium.common.exceptions.TimeoutException:
		picodash.driver.save_screenshot("./error.png")
		# instance.driver.save_screenshot("./picodash.png")
	except:
		raise
