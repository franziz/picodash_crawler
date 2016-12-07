from ..finder.location import LocationFinder

class FinderFactory:
	LOCATION = 0

	@classmethod
	def get_finder(self, finder_name=None):
		""" Exceptions:
			- AssertionError
		"""
		assert finder_name is not None, "finder_name is not defined."

		if finder_name == FinderFactory.LOCATION:
			return LocationFinder()