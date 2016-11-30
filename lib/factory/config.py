from ..config.proxy  import ProxyConfig
from ..config.sentry import SentryConfig

class ConfigFactory:
	PROXY  = 0
	SENTRY = 1

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