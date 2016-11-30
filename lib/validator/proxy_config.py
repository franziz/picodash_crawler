class ProxyConfigValidator:
	def validate(self, config=None):
		""" Exceptions:
			- AssertionError (ProxyConfig.get)
			- CannotFindField (ProxyConfig.get)
			- ValidationError
		"""
		assert config is not None, "config is not defined."

		config = config.get("proxy")
		if "ip" not in config:
			raise ValidationError("ip is not defined.")
		if "port" not in config:
			raise ValidationError("port is not defined.")
		if "database" not in config:
			raise ValidationError("database is not defined.")
		if "collection" not in config:
			raise ValidationError("collection is not defined.")