from pymongo import MongoClient
from ..      import tools

class MediaSaver(object):
	def __init__(self):
		# TODO: Move the mongodb connection string to a config and make a new class called MongoDBConnectionStringMaker that reads config file
		self.db = None
		self.db = MongoClient("mongodb://hotp:hotp7890@220.100.163.134:27017/test?authSource=hotp")
		self.db = self.db.hotp

		tools._force_create_index(self.db, "hotp_geoposts", "PostUrl")

	def save(self, media=None):
		assert self.db    is not None, "db is not defined."
		assert media      is not None, "media is not defined."

		self.db.hotp_getposts.insert_one(media)


