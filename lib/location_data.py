from pymongo import MongoClient

class LocationData(object):
	def __init__(self):
		self.db = MongoClient("mongodb://mongo:27017/test")
		self.db = self.db.hotp		

	def get_locations(self):
		assert self.db is not None, "db is not defined."

		locations = [document for document in self.db.places.find()]
		return locations
