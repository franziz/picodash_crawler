from selenium.webdriver.support    import expected_conditions as EC
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium                      import webdriver
from .                             import tools, exceptions
from .config                       import Config
import bson.json_util
import copy
import selenium
import time
import random
import arrow
import pymongo

class Picodash(object):
	def __init__(self):
		self.cookies = None
		# self.driver  = webdriver.Chrome(executable_path="./chromedriver.exe")
		self.driver  = webdriver.PhantomJS()
		self.wait    = WebDriverWait(self.driver,30)
		# self.driver.maximize_window()
		self.driver.set_window_size(1366,768)
		self.driver.get("https://www.picodash.com/")

	def quit(self):
		if self.driver is not None:
			self.driver.quit()
			self.driver = None

	def crawl(self, location_data=None, callback=None):
		try:
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
			
			print("[picodash_crawler] Location: {},{}".format(location_data["lat"], location_data["long"]))
			location_url = "https://www.picodash.com/explore/locations?location={lat}%20{long}".format(
								 lat = location_data["lat"],
								long = location_data["long"]
							)
			self.driver.get(location_url)
			# self.driver.save_screenshot("./picodash_location.png")

			# this will get all the locations listed in the URL
			self.wait.until(lambda driver:driver.find_element_by_xpath("//div[@class='grid-cell']"))
			time.sleep(random.randint(100,5000)/1000)
			locations      = self.driver.find_elements_by_xpath("//div[@class='grid-cell']")
			location_links = list()
			location_names = list()
			for location in locations:
				location_name = location.text
				location_name = location_name.replace("\n","")
				location_link = location.find_element_by_xpath(".//a")
				location_link = location_link.get_attribute("href")
				if "locations/0" not in location_link:
					location_links.append(location_link)
					location_names.append(location_name)

			# for each locations inside in the URL
			for index, link in enumerate(location_links):
				# this try and except will go to next link after one link is failed
				try:
					print("[picodash_crawler] Crawling: {}".format(location_names[index].encode("utf-8")))
					self.driver.get(link)

					# scrolling the media until it ends or hits limit of 100 scroll
					has_more = True
					max_more = 100
					tried    = 0
					while has_more:
						more  = self.driver.find_element_by_xpath("//div[@id='more']")
						style = more.get_attribute("style")
						if "display: none;" not in style and style and tried < max_more:
							more  = more.get_attribute("onclick")
							tried = tried + 1

							self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight+10)")
							time.sleep(random.randint(100,500)/1000)
						else:
							has_more = False
					#end while

					self.wait.until(lambda driver:driver.find_element_by_xpath("//div[@id='media']"))
					time.sleep(random.randint(100,5000)/1000)
					media  = self.driver.find_element_by_xpath("//div[@id='media']")
					photos = media.find_elements_by_class_name("grid-cell")
					
					for media in photos:
						# This try catch exception will skip the media if something goes wrong with the media
						try:
							# Wait until the expected dialog come to screen
							is_success = False
							while not is_success:
								try:
									dialog_to_open        = media.find_element_by_xpath("./a")
									dialog_to_open        = dialog_to_open.get_attribute("onclick")
									self.driver.execute_script(dialog_to_open)
									self.wait.until(EC.visibility_of_element_located((By.ID, "lightbox")))
									is_success = True
								except selenium.common.exceptions.TimeoutException:
									time.sleep(random.randint(100,1000)/1000)
							#end while

							btn_close      = media.find_element_by_xpath('//*[@id="lb-content"]/div[3]')
							image          = media.find_element_by_xpath("./a/img")
							user           = media.find_element_by_xpath('//div[@class="lb-title"]/a/b')
							more_info      = media.find_element_by_xpath(".//div[@class='moreInfo']/a")
							user_prof_pict = media.find_element_by_xpath('//*[@id="lb-content"]/div[7]/div[2]/a/img')
							caption        = media.find_element_by_xpath('//*[@id="lb-content"]/div[7]/div[3]')

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
								          PostSource = "INSTAGRAM"
							)
							# print(bson.json_util.dumps(media, indent=4, separators=(",",":")))
							callback(media=media)
							btn_close.click()
						except pymongo.errors.DuplicateKeyError:
							print("[picodash_crawler] Ops! Duplicate Data! {}".format(media["PostCreated_Time"]))
							break
						except ValueError:
							print("[picodash_crawler] Something wrong!")
						except selenium.common.exceptions.ElementNotVisibleException:
							print("[picodash_crawler] Something wrong!")
						except:
							raise
						#end try
					#end for
				except selenium.common.exceptions.TimeoutException:
					print(self.driver.current_url)
					print("[picodash_crawler] Timeout when go into location name! Go to next location name")
				except:
					raise
			#end for
		except selenium.common.exceptions.TimeoutException:
			print("[picodash_crawler] Request timeout!")
		except:
			print(self.driver.current_url)
			self.driver.save_screenshot("./error.png")

			self.quit()
			if "error=login" in self.driver.current_url:
				raise exceptions.LoginErrorException("I think you need to relogin!")
			raise
		finally:
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
				# self.driver.save_screenshot("ig_login.png")

				txt_username = self.driver.find_element_by_xpath("//input[@id='id_username']")
				txt_password = self.driver.find_element_by_xpath("//input[@id='id_password']")
				btn_login    = self.driver.find_element_by_xpath("//input[@type='submit']")

				tools._human_type_speed(element=txt_username, sentences=ig_username)
				tools._human_type_speed(element=txt_password, sentences=ig_password)
				btn_login.click()

				# Saving cookies when it loads perfectly			
				self.wait.until(lambda driver:driver.find_element_by_xpath('//*[@id="activeinfo"]/div[3]/a'))
				self.driver.get("https://www.picodash.com")
				cookies      = self.driver.get_cookies()
				cookies      = [cookie for cookie in cookies if "picodash" in cookie["domain"]]
				self.cookies = copy.deepcopy(cookies)
				self.quit()
				is_success  = True
			except selenium.common.exceptions.TimeoutException:
				self.quit()
				self.__init__()
				print("[picodash_crawler] Need to re-login")
				time.sleep(random.randint(1000/5000)/1000)
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
