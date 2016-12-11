from ..exceptions import ValidationError

class LoginConfigValidator:
	def validate(self, config=None):
		""" Exceptions:
			- AssertionError (LoginConfig.get)
			- CannotFindField (LoginConfig.get)
			- ValidationError
		"""
		assert config is not None, "config is not defined."

		config = config.get("login")
		if "username" not in config:
			raise ValidationError("ip is not defined.")
		if "password" not in config:
			raise ValidationError("port is not defined.")