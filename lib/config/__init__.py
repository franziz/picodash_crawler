from ..exceptions import CannotFindField
import json

class Config:
	def __init__(self, file_name=None):
		""" Exceptions:
			- AssertionError
		"""
		assert file_name is not None, "file_name is not defined."
		file           = open(file_name,"r")
		self.file_name = file_name
		self.config    = json.load(file)

	@property
	def fields(self):
		return list(self.config.keys())


	def get(self, field_name=None):
		""" Exceptions:
			- AssertionError
			- CannotFindField
		"""
		assert field_name is not None, "field_name is not defined."

		if field_name not in self.config: raise CannotFindField("Cannot find field in the config file.")
		return self.config[field_name]

	def write(self, config=None):
		""" Exceptions:
			- AssertionError
		"""
		assert config       is not None, "config is not defined."
		assert type(config) is dict    , "incorrect config data type."
		file = open(self.file_name,"w")
		file.write(json.dumps(config, indent=4))
		file.close()

	def reload(self, new_location=None):
		""" Exceptions:
			- AssertionError
		"""
		assert new_location is not None, "new_location is not defined."
		with open(new_location,"r") as file:
			self.file_name = new_location
			self.config    = json.load(file)