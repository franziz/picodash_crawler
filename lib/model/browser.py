from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui                  import WebDriverWait
from selenium   									import webdriver
import time
import random

class Browser:
	def __init__(self, url=None, proxy=None):
		""" Exceptions:
			- AssertionError (Proxy.get_proxy, self.get)
			- CannotFindField (Proxy.get_proxy)
			- ValidationError (Proxy.get_proxy)
			- NoProxyfound
		"""
		self.cookies = None

		cap                                               = DesiredCapabilities.PHANTOMJS.copy()
		cap["phantomjs.page.settings.userAgent"]          = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
		cap["phantomjs.page.settings.loadImages"]         = False
		cap["phantomjs.page.settings.webSecurityEnabled"] = False

		service_args = [
			'--ignore-ssl-errors=true',
			'--ssl-protocol=tlsv1'
		]
		if proxy is not None:
			service_args.extend(proxy.get_proxy())

		self.driver  = webdriver.PhantomJS(
			desired_capabilities = cap,
			        service_args = service_args
			)
		self.wait = WebDriverWait(self.driver,30)
		self.driver.set_window_size(1366,768)

		if url is not None:
			self.get(url)

	def get(self, url=None):
		""" Exceptions:
			- AssertionError
		"""
		assert url 		   is not None, "url is not defined."
		assert self.driver is not None, "driver is not defined."

		self.driver.get(url)

	def close(self):
		""" Exceptions:
			- AssertionError
		"""
		assert self.driver is not None, "driver is not defined."
		self.driver.quit()

	def apply_cookies(self):
		""" Exceptions:
			- AssertionError
		"""
		assert self.cookies is not None, "cookies is not defined."
		for cookie in self.cookies:
			self.driver.add_cookie(cookie)
		time.sleep(random.randint(1000,5000)/1000)

	def get_cookies(self):
		""" Exceptions:
			- AssertionError
		"""
		return self.driver.get_cookies()