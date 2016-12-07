from ..saver.post import PostSaver

class SaverFactory:
	POST = 0

	@classmethod
	def get_saver(self, saver_name=None):
		""" Exceptions:
			- AssertionError
		"""
		assert saver_name is not None, "saver_name is not defined."

		if saver_name == SaverFactory.POST:
			return PostSaver()