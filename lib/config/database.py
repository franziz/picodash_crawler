from ..factory.validator import ValidatorFactory
from . 					 import Config
import os

class DatabaseConfig(Config):
	def __init__(self):
		""" Exceptions:
			- AssertionError (__init__, DatabaseConfigValidator)
			- CannotFindField (DatabaseConfigValidator)
			- ValidationError (DatabaseConfigValidator)
		"""
		Config.__init__(self, os.path.join(".","config","database.json"))

		validator = ValidatorFactory.get_validator(ValidatorFactory.DATABASE_CONFIG)
		validator.validate(self)