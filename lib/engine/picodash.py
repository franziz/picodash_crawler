from selenium.common.exceptions import WebDriverException
from ..factory.extractor 		import ExtractorFactory
from ..model.location    		import Location
from ..model.post        		import Post
from ..model.proxy       		import Proxy
from ..model.browser     		import Browser
from ..exceptions 		 		import VerificationIsNeeded, CannotFindElements
import os
import arrow
import time
import random
import bson.json_util
import copy

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
		self.browser.driver.save_screenshot(os.path.join(os.getcwd(),"screenshot", "before_login.jpg"))

		self.browser.execute_script("loginPop()")
		extractor = ExtractorFactory.get_extractor(ExtractorFactory.XPATH)
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
		self.browser.driver.save_screenshot(os.path.join(os.getcwd(),"screenshot", "login.jpg"))
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
		self.browser.driver.save_screenshot(os.path.join(os.getcwd(),"screenshot", "after_login.jpg"))

	def crawl(self, location=None, saver=None, **kwargs):
		""" Exceptions:
			- AssertionErrror (Browser.execute_script)
			- WebDriverException
		"""
		assert location is not None, "location is not defined."
		assert saver    is not None, "saver is not defined."

		start_date = kwargs.get("start_date", arrow.now().floor("day").timestamp)
		end_date   = kwargs.get("end_date", arrow.now().ceil("day").timestamp)

		# https://www.picodash.com/explore/map#/14.6723,120.9596/1000/-
		# Go to the location
		url = "https://www.picodash.com/explore/map#/%s,%s/%s/%s-%s" % (
			location.lat,
			location.long,
			location.radius,
			end_date,
			start_date
		)
		print("Crawling: %s " % url)
		self.browser.get(url)

		# Scroll until you cannot scroll again
		has_next    = True
		start_index = 0
		while has_next:
			print("Scrolling")
			self.browser.execute_script("getMediaNextPage()")
			loading = True

			while loading:
				time.sleep(random.randint(1000,5000)/1000)
				loading = self.browser.execute_script("return loading")
				print("Loading: %s" % loading)
				loading = True if loading == 1 else False
			has_next = self.browser.execute_script("return next")
			has_next = False if has_next == 0 else True
			data = self.browser.execute_script("return dat")

			if data is None:
				data = []

			print("Current Number of Posts: %s" % len(data))
			for datum in data[start_index:]:
				post 						  = Post()
				post.track 					  = location.track
				post.city  					  = location.city
				post.country 				  = location.country
				post.post_caption_text 		  = datum["caption"]["text"] if datum["caption"] is not None else ""
				post.post_id  		   		  = datum["id"]
				post.post_std_res_picture_url = datum["images"]["standard_resolution"]["url"]
				post.post_likes   			  = datum["likes"]["count"]
				post.post_url 				  = datum["link"]
				post.post_geolocation		  = Location(
													 lat = datum["location"]["latitude"],
													long = datum["location"]["longitude"],
													name = datum["location"]["name"],
													  id = datum["location"]["id"]
												)
				post.post_tags 				  = datum["tags"]
				post.post_from_user_id        = datum["user"]["id"]
				post.post_from_username 	  = datum["user"]["username"]
				post.post_user_profile_pic    = datum["user"]["profile_picture"]
				post.query_search_location    = copy.deepcopy(location)
				post.post_created_time  	  = arrow.get(datum["created_time"]).format("YYYY-MM-DD HH:mm:ss")
				post.post_inserted_date       = arrow.now().format("YYYY-MM-DD")
				post.post_inserted_date_iso   = arrow.utcnow().datetime

				saver.save(post)
			start_index = len(data)