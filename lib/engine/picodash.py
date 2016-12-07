from ..factory.extractor import ExtractorFactory
from ..model.proxy       import Proxy
from ..model.browser     import Browser
from ..exceptions 		 import VerificationIsNeeded, CannotFindElements

class PicodashEngine:
	def __init__(self, **kwargs):
		self.proxy    = kwargs.get("proxy", Proxy())
		self.browser  = Browser(proxy=self.proxy)
		self.username = kwargs.get("username", None)
		self.password = kwargs.get("password", None)

	def show_instagram_login(self):
		""" Exceptions:
			- AssertionError (Browser.get, XPATHExtractor.extract)
			- CannotFindElements (XPATHExtractor.extract)
		"""
		self.browser.get("https://www.picodash.com/")

		extractor = ExtractorFactory.get_extractor(ExtractorFactory.XPATH)
		btn_login = extractor.extract(
			browser = self.browser,
			  xpath = '//*[@id="loginTab"]',
			   wait = '//*[@id="loginTab"]'
		)
		btn_login.click()
		
		btn_yes = extractor.extract(
			browser = self.browser,
			  xpath = '//*[@id="lb-popup"]/div/a[1]',
			   wait = '//*[@id="lb-popup"]/div/a[1]'
		)
		btn_yes.click()

	def instagram_login(self, username=None, password=None):
		""" Exceptions:
			- AssertionError (XPATHExtractor.extract)
			- CannotFindElements (XPATHExtractor.extract)\
			- VerificationIsNeeded
		"""
		assert username is not None, "username is not defined."
		assert password is not None, "password is not defined."

		extractor    = ExtractorFactory.get_extractor(ExtractorFactory.XPATH)
		txt_username = extractor.extract(
			browser = self.browser,
			  xpath = '//*[@id="id_username"]',
			   wait = '//*[@id="id_username"]'
		)
		txt_username.send_keys(username)

		txt_password = extractor.extract(
			browser = self.browser,
			  xpath = '//*[@id="id_password"]',
			   wait = '//*[@id="id_password"]'
		)
		txt_password.send_keys(password)

		btn_login = extractor.extract(
			browser = self.browser,
			  xpath = '//*[@id="login-form"]/p[3]/input',
			   wait = '//*[@id="login-form"]/p[3]/input'
		)
		btn_login.click()

		try:
			# Checking do I need to verify my account or not
			need_to_verify = extractor.extract(
				  browser = self.browser,
					xpath = '/html/body/div/section/div/p',
					 wait = '/html/body/div/section/div/p',
				max_retry = 1
			)
			if need_to_verify.text == "Verify Your Account":
				raise VerificationIsNeeded("You need to verify your account")
			print(need_to_verify.text)
		except CannotFindElements as ex:
			pass

		btn_go_to_dashboard = extractor.extract(
			browser = self.browser,
			  xpath = '//*[@id="actioninfo"]/a',
			   wait = '//*[@id="actioninfo"]/a'
		)

	def login(self):
		""" Exceptions:
			- AssertionError (self.show_instagram_login, self.instagram_login)
			- CannotFindElements (self.show_instagram_login, self.instagram_login)
			- VerificationIsNeeded (self.instagram_login)
		"""
		assert self.username is not None, "username is not defined."
		assert self.password is not None, "password is not defined."

		self.show_instagram_login()
		self.instagram_login(self.username, self.password)
		self.browser.driver.save_screenshot("after_login.jpg")


	def crawl(self, location=None, saver=None, **kwargs):
		""" Exceptions:
			- AssertionErrror
		"""
		assert location is not None, "location is not defined."
		assert saver    is not None, "saver is not defined."

		start_date = kwargs.get("start_date", "")
		end_date   = kwargs.get("end_date","")

		# https://www.picodash.com/explore/map#/14.6723,120.9596/1000/-
		# Go to the location
		self.browser.get("https://www.picodash.com/explore/map#/%s,%s/%s/%s-%s" % (
			location.lat,
			location.long,
			location.radius,
			start_date,
			end_date
		))

		extractor   = ExtractorFactory.get_extractor(ExtractorFactory.XPATH)
		total_posts = extractor.extract(
			browser = self.browser,
			  xpath = '//div[@id="counter"]',
			   wait = '//div[@id="counter"]'
		)
		total_posts = total_posts.text

		print("Total Posts: %s" % total_posts)