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

from picodash import Picodash
from selenium import webdriver
import selenium
import _thread
import copy
import bson.json_util

def callback(media=None):
	assert media is not None, "media is not defined."
	print(bson.json_util.dumps(media, indent=4, separators=(",",":")))
#end def

def execute_thread(cookies=None):	
	assert cookies is not None, "cookies is not defined."

	picodash         = Picodash()
	picodash.cookies = cookies
	picodash.apply_cookies()
	instance.crawl(location_data=MOCK_INPUT, callback=callback)		

try:
	picodash = Picodash()
	picodash.login(
		ig_username = "amoure20",
		ig_password = "081703706966"
	)	
	# instance = picodash.new_instance()
	# instance.crawl(location_data=MOCK_INPUT, callback=callback)		
	_thread.start_new_thread(execute_thread,(picodash.cookies,))
	# _thread.start_new_thread(execute_thread,(picodash,))
	# _thread.start_new_thread(execute_thread,(picodash,))

	while 1:
		pass
except selenium.common.exceptions.TimeoutException:
	instance.driver.save_screenshot("./picodash.png")
except:
	raise
