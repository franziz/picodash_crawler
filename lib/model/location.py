import copy 

class Location:
	def __init__(self, **kwargs):
		self.source = kwargs.get("source", None)
		self.id     = kwargs.get("id", None)
		self.lat    = kwargs.get("lat", None)
		self.long   = kwargs.get("long", None)
		self.radius = kwargs.get("radius", 1000)

		if self.source is not None:
			self.id   = copy.deepcopy(self.source["_id"])
			self.lat  = copy.deepcopy(self.source["lat"])
			self.long = copy.deepcopy(self.source["long"])

	def update_status(self, status=None):
		""" Exceptions:
			- AssertionError
		"""
		assert status  is not None, "status is not defined."
		assert self.id is not None, "id is not defined."

		conn = pymongo.MongoClient("mongodb://hotp:hotp7890@220.100.163.134:27017/hotp?authSource=hotp")
		db   = conn["hotp"]
		db.places_sparse.update(
			{"_id": self.id},
			{"$set": {"status": status}}
		)
		conn.close()

	def set_as_idle(self):
		""" Exceptions:
			- AssertionError (self.update_status)
		"""
		self.update_status("idle")

	def set_as_processing(self):
		""" Exceptions:
			- AssertionError (self.update_status)
		"""
		self.update_status("processing")

	def set_processed(self):
		""" Exceptions:
			- AssertionError (self.update_status)
		"""
		self.update_status("processed")