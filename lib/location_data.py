from pymongo import MongoClient
import pymongo

class LocationData(object):
	def __init__(self):
		self._connect()

	def _connect(self):
		# TODO: Move the mongodb connection string to a config and make a new class called MongoDBConnectionStringMaker that reads config file
		self.db              = MongoClient("mongodb://hotp:hotp7890@220.100.163.134:27017/test?authSource=hotp")
		self.db              = self.db.hotp
		self.collection_name = "places_sparse"


	def _update_status(self, _id=None, status=None):
		success = False
		while not success:
			try:
				assert _id     is not None, "_id is not defined."
				assert status  is not None, "status is not defined."
				assert self.db is not None, "db is not defined."
				self.db[self.collection_name].update_one({"_id":_id},{"$set":{"status":status}})
				success = True
			except pymongo.errors.AutoReconnect:
				self._connect()
			except:
				raise
	#end def


	def get_locations(self, all=False):
		assert self.db is not None, "db is not defined."

		if not all:
			conditions = [
							{"status":"idle"},
							{"status":"processing"},
							{"status":None}
						 ]
			locations  = self.db[self.collection_name].find({"$or":conditions, "$and":[{"is_active":True}]})
		else:
			locations = self.db[self.collection_name].find({"is_active":True})
		locations = [document for document in locations]

		if len(locations) == 0 and not all:
			locations = self.get_locations(all=True)
			for location in locations: self.set_as_idle(location)
			locations = self.get_locations()
		return locations

	def set_as_idle(self, location=None):
		assert location is not None, "location is not defined."
		assert "_id"    in location, "_id is not defined."
		self._update_status(location["_id"], "idle")

	def set_as_processed(self, location=None):
		assert location is not None, "location is not defined."
		assert "_id"    in location, "_id is not defined."
		self._update_status(location["_id"], "processed")

	def set_as_processing(self, location=None):
		assert location is not None, "location is not defined."
		assert "_id"    in location, "_id is not defined."
		self._update_status(location["_id"], "processing")