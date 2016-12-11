# from ..model.location import Location
# import pymongo

# class LocationFinder:
# 	def find(self):
# 		return [Location(lat=-7.2741, long=112.6449)]

from ..model.location import Location
import pymongo

class LocationFinder:
	def find(self):
		conn = pymongo.MongoClient("mongodb://hotp:hotp7890@220.100.163.134:27017/hotp?authSource=hotp")
		db   = conn["hotp"]

		docs = db.places_sparse.find({
			"$or":[
				{"status": "idle"},
				{"status": "processing"},
				{"status": None}
			],
			"$and": [
				{"is_active": True}
			]
		})

		result = [Location(source=doc) for doc in docs]
		conn.close()

		if len(result) == 0:
			result = self.find_all()
			for loc in result:
				loc.set_as_idle()
		return result

	def find_all(self):
		conn = pymongo.MongoClient("mongodb://hotp:hotp7890@220.100.163.134:27017/hotp?authSource=hotp")
		db   = conn["hotp"]
		docs = db.places_sparse.find({"is_active": True})
		conn.close()
		return [Location(source=doc) for doc in docs]