from raven.conf 		    import setup_logging
from raven.handlers.logging import SentryHandler
from ..factory.config       import ConfigFactory
import raven
import logging

class Logger(raven.Client):
	def __init__(self, **kwargs):
		""" Exceptions:
			- AssertionError (SentryConfig)
			- CannotFindField (SentryConfig)
		"""
		config = ConfigFactory.get_config(ConfigFactory.SENTRY)
		config = config.get("sentry")

		self.public_key = config["public_key"]
		self.secret_key = config["secret_key"]
		self.project_id = config["project_id"]
		self.port       = config["port"]
		self.ip         = config["ip"]

		self.dsn = "http://%s:%s@%s:%s/%s" % (
			self.public_key,
			self.secret_key,
			self.ip,
			self.port,
			self.project_id
		)
		raven.Client.__init__(self, self.dsn, auto_log_stacks=True, **kwargs)

		self.handler = SentryHandler(self)
		setup_logging(self.handler)