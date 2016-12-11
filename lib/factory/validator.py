from ..validator.proxy_config    import ProxyConfigValidator
from ..validator.sentry_config   import SentryConfigValidator
from ..validator.login_config    import LoginConfigValidator
from ..validator.database_config import DatabaseConfigValidator

class ValidatorFactory:
	PROXY_CONFIG    = 0
	SENTRY_CONFIG   = 1
	LOGIN_CONFIG    = 2
	DATABASE_CONFIG = 3

	@classmethod
	def get_validator(self, validator_name=None):
		""" Exceptions: 
			- AssertionError
		"""
		assert validator_name is not None, "validator_name is not defined."

		if validator_name == ValidatorFactory.PROXY_CONFIG:
			return ProxyConfigValidator()
		elif validator_name == ValidatorFactory.SENTRY_CONFIG:
			return SentryConfigValidator()
		elif validator_name == ValidatorFactory.LOGIN_CONFIG:
			return LoginConfigValidator()
		elif validator_name == ValidatorFactory.DATABASE_CONFIG:
			return DatabaseConfigValidator()