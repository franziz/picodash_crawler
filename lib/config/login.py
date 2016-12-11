from ..factory.validator import ValidatorFactory
from . 					 import Config
import os

class LoginConfig(Config):
	def __init__(self):
		""" Exceptions:
			- AssertionError (__init__, LoginConfigValidator)
			- CannotFindField (LoginConfigValidator)
			- ValidationError (LoginConfigValidator)
		"""
		Config.__init__(self, os.path.join(".","config","login.json"))

		validator = ValidatorFactory.get_validator(ValidatorFactory.LOGIN_CONFIG)
		validator.validate(self)