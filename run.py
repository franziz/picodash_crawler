from pymongo      import MongoClient
from lib.executor import Runner
from lib.engine   import Engine
import _thread
import time
import random

def execute_runner(document=None):
	assert document is not None, "document is not defined."

	runner = Runner()
	runner.run(
		   place = document,
		username = "xzerocool",
		password = "isidsea",
		  driver = Engine.PHANTOMJS
	)
	global current_thread
	current_thread = current_thread - 1
#end def

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
		time.sleep(random.randint(10,500)/1000)

	_thread.start_new_thread(execute_runner, (document,))
	current_thread = current_thread + 1