from ..engine  import Engine
from ..        import tools
from pymongo    import MongoClient
import bson.json_util
import pymongo

class Runner(object):
	def __init__(self):
		self.db = MongoClient("mongodb://isid:isid123@192.168.1.14:27017/?authSource=admin")
		self.db = self.db.hotp
		tools._force_create_index(self.db,"picodash_test","PostUrl")

	def _callback(self,media=None):
		assert media is not None, "media is not defined."
		try:
			self.db.picodash_test.insert_one(media)
			# print(bson.json_util.dumps(media, indent=4, separators=(",",":")))
			print("[picodas_crawler] Inserted one document!")
		except pymongo.errors.DuplicateKeyError:
			print("[picodash_crawler] Duplicate Data!")

	def run(self, place=None, username=None, password=None, driver=Engine.CHROME):
		assert username is not None, "username is not defined."
		assert password is not None, "password is not defined."
		assert place    is not None, "place is not defined."

		engine             = Engine(driver=driver)
		engine.INPUT       = place
		engine.ig_username = username
		engine.ig_password = password
		engine.crawl(self._callback)