from ..exceptions import ValidationError

class SentryConfigValidator:
	def validate(self, config=None):
		""" Exceptions:
			- AssertionError (SentryConfig.get)
			- CannotFindField (SentryConfig.get)
		"""
		assert config is not None, "config is not defined."

		config = config.get("sentry")
		if "public_key" not in config:
			raise ValidationError("public_key is not defined.")
		if "secret_key" not in config:
			raise ValidationError("secret_key is not defined.")
		if "ip" not in config:
			raise ValidationError("ip is not defined.")
		if "port" not in config:
			raise ValidationError("port is not defined.")
		if "project_id" not in config:
			raise ValidationError("project_id is not defined.")