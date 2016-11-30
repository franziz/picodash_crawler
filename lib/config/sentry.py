from ..factory.validator import ValidatorFactory
from . 					 import Config
import os

class SentryConfig(Config):
	def __init__(self):
		""" Exceptions:
			- AssertionError (SentryConfigValidator)
			- CannotFindField (SentryConfigValidator)
		"""
		Config.__init__(self, os.path.join(".","config","sentry.json"))

		validator = ValidatorFactory.get_validator(ValidatorFactory.SENTRY_CONFIG)
		validator.validate(self)