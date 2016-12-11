from ..config.proxy    import ProxyConfig
from ..config.sentry   import SentryConfig
from ..config.login    import LoginConfig
from ..config.database import DatabaseConfig

class ConfigFactory:
	PROXY    = 0
	SENTRY   = 1
	LOGIN    = 2
	DATABASE = 3

	@classmethod
	def get_config(self, config_name=None):
		""" Exceptions: 
			- AssertionError
		"""
		assert config_name is not None, "config_name is not defined."

		if config_name == ConfigFactory.PROXY:
			return ProxyConfig()
		elif config_name == ConfigFactory.SENTRY:
			return SentryConfig()
		elif config_name == ConfigFactory.LOGIN:
			return LoginConfig()
		elif config_name == ConfigFactory.DATABASE:
			return DatabaseConfig()