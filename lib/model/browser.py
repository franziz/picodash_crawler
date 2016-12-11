from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui                  import WebDriverWait
from selenium.webdriver.support					    import expected_conditions as EC
from selenium.common.exceptions 					import TimeoutException
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

		# PHANTOMJS
		cap                                               = DesiredCapabilities.PHANTOMJS.copy()
		cap["phantomjs.page.settings.userAgent"]          = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
		cap["phantomjs.page.settings.loadImages"]         = False
		cap["phantomjs.page.settings.webSecurityEnabled"] = False

		service_args = [
			'--ignore-ssl-errors=true',
			'--ssl-protocol=tlsv1'
		]
		if proxy is not None:
			self.proxy = proxy.get_proxy()
			service_args.append("--proxy=%s:%s" % (self.proxy.ip, self.proxy.port))
			service_args.append("--proxy-auth=%s:%s" % (self.proxy.username, self.proxy.password))
			service_args.append("--proxy-type=http")

		self.driver  = webdriver.PhantomJS(
		desired_capabilities = cap,
		        service_args = service_args
		)

		# FIREFOX
		# firefox_profile = webdriver.FirefoxProfile()
		# firefox_profile.set_preference('permissions.default.image', 2)
		# firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

		# if proxy is not None:
		# 	self.proxy = proxy.get_proxy()
		# 	firefox_profile.set_preference("network.proxy.http", self.proxy.ip)
		# 	firefox_profile.set_preference("network.proxy.http.port", self.proxy.port)
		# 	firefox_profile.set_preference("network.proxy.type", 1)
		# 	firefox_profile.set_preference("signon.autologin.proxy", True)

		# self.driver = webdriver.Firefox(firefox_profile=firefox_profile)
		self.wait   = WebDriverWait(self.driver,30)
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
		# try:
		# 	WebDriverWait(self.driver, 3).until(EC.alert_is_present())
		# 	self.driver.save_screenshot("test.jpg")
		# 	alert = self.driver.switch_to_alert()
		# 	alert.send_keys(self.proxy.username)
		# 	alert.send_keys(Keys.TAB)
		# 	alert.send_keys(self.proxy.password)
		# 	alert.accept()
		# except TimeoutException:
		# 	self.driver.save_screenshot("no-alert.jpg")
		# 	print("No Alert")

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

	def get_cookies(self):
		""" Exceptions:
			- AssertionError
		"""
		return self.driver.get_cookies()

	def execute_script(self, script=None):
		""" Exception:
			- AssertionError
		"""
		assert script is not None, "script is not defined."
		return self.driver.execute_script(script)