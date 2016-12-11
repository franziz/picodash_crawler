from ..exceptions import ValidationError

class DatabaseConfigValidator:
	def validate(self, config=None):
		""" Exceptions:
			- AssertionError (DatabaseConfig.get)
			- CannotFindField (DatabaseConfig.get)
			- ValidationError
		"""
		assert config is not None, "config is not defined."

		for field in config.fields:
			database = config.get(field)

			if "connectionString" not in database:
				raise ValidationError("connectionString is not defined.")

			if "collection" not in database:
				raise ValidationError("collection is not defined.")

			if "database" not in database:
				raise ValidationError("database is not defined.")