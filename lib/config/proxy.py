from ..factory.validator import ValidatorFactory
from . 					 import Config
import os

class ProxyConfig(Config):
	def __init__(self):
		""" Exceptions:
			- AssertionError (__init__, ProxyConfigValidator)
			- CannotFindField (ProxyConfigValidator)
			- ValidationError (ProxyConfigValidator)
		"""
		Config.__init__(self, os.path.join(".","config","proxy.json"))

		validator = ValidatorFactory.get_validator(ValidatorFactory.PROXY_CONFIG)
		validator.validate(self)