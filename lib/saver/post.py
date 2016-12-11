from lib.factory.config import ConfigFactory
import pymongo

class PostSaver:
	def save(self, post=None):
		""" Exceptions:
			- AssertionError
		"""
		assert post is not None, "post is not defined."

		config = ConfigFactory.get_config(ConfigFactory.DATABASE)
		config = config.get("postSaver")

		conn = pymongo.MongoClient(config["connectionString"])
		db   = conn[config["database"]]


		try:
			db[config["collection"]].create_index("PostUrl", background=True, unique=True, sparse=True)
			db[config["collection"]].insert(post.to_dict())
			print("[success] Inserted one document!")
		except pymongo.errors.DuplicateKeyError:
			print("[error] Duplicate document!")
		conn.close()