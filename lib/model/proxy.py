from ..factory.config import ConfigFactory
from ..exceptions     import NoProxyFound
import pymongo
import random
import copy

class Proxy:
	def __init__(self):
		self.ip 	  = None
		self.port 	  = None
		self.username = None
		self.password = None

	def get_proxy(self):
		""" Exceptions:
			- AssertionError (ProxyConfig)
			- CannotFindField (ProxyConfig)
			- ValidationError (ProxyConfig)
			- NoProxyfound
		"""
		factory = ConfigFactory.get_config(ConfigFactory.PROXY)
		config  = factory.get("proxy")

		conn = pymongo.MongoClient("mongodb://%s:%s/%s" % (
			config["ip"],
			config["port"],
			config["database"]
		))
		db    = conn[config["database"]]
		docs  = db[config["collection"]].find({})

		if docs.count() == 0:
			raise NoProxyFound("Cannot find proxy given configuration.")
		docs  = [doc for doc in docs]
		proxy = random.sample(docs,1)[0]

		self.ip 	  = proxy["ip"]
		self.port 	  = proxy["port"]
		self.username = proxy["username"]
		self.password = proxy["password"]

		return copy.deepcopy(self)

		# return [
		# 	"--proxy=%s:%s" % (self.proxy["ip"], self.proxy["port"]),
		# 	"--proxy-auth=%s:%s" % (self.proxy["username"], self.proxy["password"]),
		# 	"--proxy-type=http"
		# ]