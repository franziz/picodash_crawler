from selenium.webdriver.support    import expected_conditions as EC
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium                      import webdriver
from ..                            import tools, exceptions
from ..config                      import Config
from ..media.extractor             import MediaExtractor
from .location_extractor           import LocationExtractor
from .browser_tools                import BrowserTools
import bson.json_util
import copy
import selenium
import time
import random
import arrow
import pymongo
import pyprind

class Picodash(object):
	def __init__(self):
		self.cookies       = None		
		self.driver        = webdriver.PhantomJS()
		self.wait          = WebDriverWait(self.driver,30)
		self.browser_tools = BrowserTools(self.driver)		
		self.driver.set_window_size(1366,768)
		self.driver.get("https://www.picodash.com/")

	def quit(self):
		if self.driver is not None:
			self.driver.quit()
			self.driver = None

	def crawl(self, location_data=None, callback=None):
		assert self.browser_tools  is not None     , "browser_tools is not defined."
		assert self.driver         is not None     , "driver is not defined."
		assert self.wait           is not None     , "wait is not defined."
		assert callback            is not None     , "callback is not defined."
		assert location_data       is not None     , "location_data is not defined."
		assert type(location_data) is dict         , "location_data should be a dict data type."
		assert "lat"               in location_data, "cannot find 'lat' in location_data."
		assert "long"              in location_data, "cannot find 'long' in location_data."
		assert "track"             in location_data, "cannot find 'track' in location_data."
		assert "city"              in location_data, "cannot find 'city' in location_data."
		assert "country"           in location_data, "cannot find 'country' in location_data."
		assert "name"              in location_data, "cannot find 'name' in location_data."
		assert "category"          in location_data, "cannot find 'category' in location_data."
		
		location_extractor = LocationExtractor(self.driver)
		locations          = location_extractor.extract(
								 lat = location_data["lat"],
								long = location_data["long"]
							 )
		# for each locations inside in the URL
		for index, location in enumerate(locations):
			crawled = False			
			link    = location["link"]
			name    = location["name"]
			print("[picodash_crawler] Crawling: {}".format(name.encode("utf-8")))
			self.driver.get(link)					
			self.browser_tools.scroll(max_scroll=4)

			media_extractor = MediaExtractor(self.driver)
			photos          = media_extractor.extract()
			print("[picodash_crawler] Got {} photos".format(len(photos)))
			for media in photos:
				# This try catch exception will skip the media if something goes wrong with the media
				try:
					# Wait until the expected dialog come to screen
					loaded = False
					while not loaded:
						try:
							dialog_to_open        = media.find_element_by_xpath("./a")
							dialog_to_open        = dialog_to_open.get_attribute("onclick")
							self.driver.execute_script(dialog_to_open)
							self.wait.until(EC.visibility_of_element_located((By.ID, "lightbox")))
							loaded = True
						except selenium.common.exceptions.TimeoutException:
							time.sleep(random.randint(100,1000)/1000)

					btn_close      = media.find_element_by_xpath('//*[@id="lb-content"]/div[3]')
					image          = media.find_element_by_xpath("./a/img")
					user           = media.find_element_by_xpath('//div[@class="lb-title"]/a/b')
					more_info      = media.find_element_by_xpath(".//div[@class='moreInfo']/a")
					user_prof_pict = media.find_element_by_xpath('//*[@id="lb-content"]/div[7]/div[2]/a/img')
					caption        = media.find_element_by_xpath('//*[@id="lb-content"]/div[7]/div[4]')
					
					tags           = media.find_elements_by_xpath('//*[@id="lb-content"]/div[7]/div[3]//a')
					tags           = [tag.text for tag in tags if "tags" in tag.get_attribute("href")]
					
					metadata_info  = media.find_element_by_xpath("//div[@class='lb-commentDate']")
					metadata_info  = metadata_info.text
					metadata_info  = metadata_info.split("|")
					
					assert len(metadata_info) > 0, "Cannot find metadata_info."
					published_date = metadata_info[0]
					published_date = published_date[published_date.index("(")+1:-2]
					published_date = tools._date_parser(published_date)

					current_url    = self.driver.current_url
					ig_url         = media.find_element_by_xpath("//div[@class='lb-links']/div[1]/a").get_attribute("href")

					media          = dict(
						               Track = location_data["track"],
						                City = location_data["city"].strip(),
						             Country = location_data["country"],
						     PostCaptionText = caption.text.split("\n")[0],
						              PostId = media.get_attribute("class").split(" ")[1],
						PostStdResPictureUrl = image.get_attribute("src"),
						           PostLikes = media.get_attribute("data-likes"),
						             PostUrl = ig_url,
						     PostGeolocation = dict(
													  latitude = "",
													      name = metadata_info[2].strip(),
													longtitude = "",
													        id = current_url.split("/")[5]
												),
						            PostTags = tags,
						            PostType = "image",
						      PostFromUserId = media.get_attribute("class").split(" ")[1].split("_")[1],
						    PostFromUsername = user.text,
						  PostUserProfilePic = user_prof_pict.get_attribute("src"),
						 QuerySearchLocation = dict(
													    name = location_data["name"],
													     lat = location_data["lat"],
													    long = location_data["long"],
													category = location_data["category"],
													   track = location_data["track"]	
												),
						    PostCreated_Time = "{}-{}-{}".format(published_date.year, str(published_date.month).zfill(2), str(published_date.day).zfill(2)),
						   PostInserted_Date = "{}-{}-{}".format(arrow.now().year, str(arrow.now().month).zfill(2), str(arrow.now().day).zfill(2)),
					   PostInserted_Date_ISO = arrow.now().datetime,
						          PostSource = "INSTAGRAM"
					)
					# print(bson.json_util.dumps(media, indent=4, separators=(",",":")))
					callback(media=media)
					btn_close.click()
				except ValueError:
					# this exception happens when published_date could not be found.
					# this just say "substring not found"
					print("[picodash_crawler] ValueError")
					pass
				except selenium.common.exceptions.ElementNotVisibleException:
					# when btn_close cannot be clicked
					print("[picodash_crawler] ElementNotVisibleException.")
					pass
				except exceptions.DuplicateData:
					break
				except AssertionError:
					print("[picodash_crawler] Assertion is not satisfied.")									
			#end for
		#end for
		self.quit()	
	#end def

	def login(self):
		assert self.driver is not None, "driver is not defined."
		assert self.wait   is not None, "wait is not defined."

		is_success = False
		while not is_success:
			try:
				config = Config()
				config = config.config

				assert "ig"       in config      , "ig is not defined."
				assert "username" in config["ig"], "username is not defined."
				assert "password" in config["ig"], "password is not defined."

				ig_username = config["ig"]["username"]
				ig_password = config["ig"]["password"]

				print("[picodash_crawler] Login-ing")

				btn_login = self.driver.find_element_by_xpath('//*[@id="infobar"]/div[2]/a[1]')
				btn_login.click()

				self.wait.until(lambda driver:driver.find_element_by_xpath("//input[@id='id_username']"))

				txt_username = self.driver.find_element_by_xpath("//input[@id='id_username']")
				txt_password = self.driver.find_element_by_xpath("//input[@id='id_password']")
				btn_login    = self.driver.find_element_by_xpath("//input[@type='submit']")

				tools._human_type_speed(element=txt_username, sentences=ig_username)
				tools._human_type_speed(element=txt_password, sentences=ig_password)
				btn_login.click()

				# Saving cookies when it loads perfectly
				self.driver.get("https://www.picodash.com/fransisid8117")
				is_success = False if "error=login" in self.driver.current_url else True

				if is_success:
					cookies      = self.driver.get_cookies()
					cookies      = [cookie for cookie in cookies if "picodash" in cookie["domain"]]
					self.cookies = copy.deepcopy(cookies)
					self.quit()
				else:
					print("[picodash_crawler] {}".format(self.driver.current_url.encode("utf-8")))
					self.driver.save_screenshot("login_error.png")
					self.quit()
					self.__init__()
					print("[picodash_crawler] Need to re-login")
					time_to_wait = random.randint(300,600)
					tools._wait(duration=time_to_wait)
			except:
				self.quit()
				raise
		#end while
	#end def

	def apply_cookies(self):
		assert self.cookies is not None, "cookies is not defined."

		for cookie in self.cookies:
			self.driver.add_cookie(cookie)
		time.sleep(random.randint(1000,5000)/1000)
		self.driver.get("https://www.picodash.com")
