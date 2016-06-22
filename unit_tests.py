from pymongo      import MongoClient
from lib.executor import Runner
from lib.engine   import Engine
import _thread

def execute_runner(document=None):
	assert document is not None, "document is not defined."
	print(document)

	global current_thread
	current_thread = current_thread - 1

db        = MongoClient("mongodb://isid:isid123@192.168.1.14/?authSource=admin")
db        = db.hotp

documents = list()
for document in db.places.find():
	documents.append(dict(
		     name = document["name"],
		      lat = document["lat"],
		     long = document["long"],
		 category = document["category"],
		    track = document["track"],
		     city = document["city"],
		  country = document["country"],
		processed = document["processed"],
		  address = document["address"]
	))
#end for

global current_thread
current_thread = 0
max_thread     = 10
for document in documents:
	while current_thread >= max_thread:
		time.sleep(random.randint(10/500)/1000)

	_thread.start_new_thread(execute_runner, (document))
	current_thread = current_thread + 1

# MOCK_INPUT = {
# 	     "name":" autogenPointII 1",
# 	      "lat":"14.6526527",
# 	     "long":"120.881398",
# 	 "category":"blanketCover",
# 	    "track":"MakatiBlanket",
# 	     "city":"Makati",
# 	  "country":"Philippines",
# 	"processed":"FALSE",
# 	  "address":""
# }

# from lib.executor import Runner
# from lib.engine   import Engine

# runner = Runner()
# runner.run(
# 	   place = MOCK_INPUT,
# 	username = "xzerocool",
# 	password = "isidsea",
# 	  driver = Engine.CHROME
# )


# from engine  import Engine
# from pymongo import MongoClient
# import bson.json_util
# import pymongo
# import tools

# global db
# db = MongoClient("mongodb://isid:isid123@192.168.1.14:27017/?authSource=admin")
# db = db.hotp
# tools._force_create_index(db,"picodash_test","PostUrl")


# def callback(media=None):
# 	assert media is not None, "media is not defined."
# 	try:
# 		db.picodash_test.insert_one(media)
# 		# print(bson.json_util.dumps(media, indent=4, separators=(",",":")))
# 		print("[picodas_crawler] Inserted one document!")
# 	except pymongo.errors.DuplicateKeyError:
# 		print("[picodash_crawler] Duplicate Data!")

# engine             = Engine(driver=Engine.CHROME)
# engine.INPUT       = MOCK_INPUT
# engine.ig_username = "xzerocool"
# engine.ig_password = "isidsea"
# engine.crawl(callback)