from pymongo import MongoClient

class LocationData(object):
	def __init__(self):
		# TODO: Move the mongodb connection string to a config and make a new class called MongoDBConnectionStringMaker that reads config file
		self.db = MongoClient("mongodb://hotp:hotp7890@220.100.163.134:27017/test?authSource=hotp")
		self.db = self.db.hotp		

	def get_locations(self):
		assert self.db is not None, "db is not defined."

		locations = [document for document in self.db.places_sparse.find()]
		return locations
