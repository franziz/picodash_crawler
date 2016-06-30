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

from lib.location_data   import LocationData
from lib.picodash.engine import Picodash
from lib.media.saver     import MediaSaver
from lib.exceptions      import LoginErrorException, DuplicateData
from selenium            import webdriver
from pymongo             import MongoClient
import selenium
import bson.json_util
import multiprocessing
import pymongo
import pyprind

def callback(media=None):
	assert media is not None, "media is not defined."
	try:
		media_saver = MediaSaver()
		media_saver.save(media)
		print("[picodash_crawler] Inserted one document!")
	except pymongo.errors.DuplicateKeyError:
		print("[picodash_crawler] Ops! Duplicate Data! {}".format(media["PostCreated_Time"]))
		raise DuplicateData("Duplicate data on database.")

	# print(bson.json_util.dumps(media, indent=4, separators=(",",":")))
#end def

def execute_thread(data=None):	
	current = multiprocessing.current_process()
	db      = MongoClient("mongodb://mongo:27017/test")
	db      = db.monitor

	try:	
		assert data is not None, "data is not defined."
		print("[picodash_crawler] Engine start!")

		db.pico_worker.update({"name":current.name},{"$set":{
			  "name" : current.name,
			"status" : "working"
		}},upsert=True)

		location_data    = data[0]
		cookies          = data[1]

		picodash         = Picodash()
		picodash.cookies = cookies
		picodash.apply_cookies()
		picodash.crawl(location_data=location_data, callback=callback)

		db.pico_worker.update({"name":current.name},{"$set":{
			  "name" : current.name,
			"status" : "finished"
		}},upsert=True)

		print("[picodash_crawler] Crawler DEAD!")
	except AssertionError:
		print("[picodash_crawler] Assertion is not satisfied.")

if __name__ == "__main__":	
	picodash           = Picodash()
	picodash.login()

	location_data = LocationData()
	locations     = location_data.get_locations()
	print("[picodash_crawler] Number of Locations: {}".format(len(locations)))
	
	locations     = [(location, picodash.cookies) for location in locations]
	multi_process = multiprocessing.Pool(20)
	multi_process.map(execute_thread, locations)
