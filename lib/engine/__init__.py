from selenium.webdriver.support.ui import WebDriverWait
from selenium                      import webdriver
from selenium.webdriver.support    import expected_conditions as EC
from selenium.webdriver.common.by  import By
from ..                            import tools
import time
import random
import selenium
import arrow

class Engine(object):
	def __init__(self, driver=None):
		assert driver       is not None, "driver is not defined."
		assert type(driver) is property, "driver should be an property from Engine."

		self.SELECTED_DRIVER = driver
		self.INPUT           = None
		self.driver          = None
		self.wait            = None
		self.ig_username     = None
		self.ig_password     = None

		self._init_driver()
	#end def

	@property
	def FIREFOX(self): return 1
	
	@property
	def PHANTOMJS(self): return 2

	@property
	def CHROME(self): return 3

	def _init_driver(self):
		if self.SELECTED_DRIVER == Engine.CHROME:
			self.driver = webdriver.Chrome(executable_path="./chromedriver.exe")
			self.driver.maximize_window()
		elif self.SELECTED_DRIVER == Engine.FIREFOX:
			self.driver = webdriver.Firefox()
			self.driver.maximize_window()
		elif self.SELECTED_DRIVER == Engine.PHANTOMJS:
			self.driver = webdriver.PhantomJS()
			self.driver.set_window_size(1366,768)
		self.wait = WebDriverWait(self.driver,10)
	#end def

	def crawl(self, callback=None):
		assert callback         is not None  , "callback is not defined."
		assert self.driver      is not None  , "driver is not defined."
		assert self.wait        is not None  , "wait is not defined."
		assert self.ig_username is not None  , "ig_username is not defined."
		assert self.ig_password is not None  , "ig_password is not defined."
		assert self.INPUT       is not None  , "INPUT is not defined."
		assert type(self.INPUT) is dict      , "INPUT should be a dict data type."
		assert "lat"            in self.INPUT, "cannot find 'lat' in INPUT."
		assert "long"           in self.INPUT, "cannot find 'long' in INPUT."
		assert "track"          in self.INPUT, "cannot find 'track' in INPUT."
		assert "city"           in self.INPUT, "cannot find 'city' in INPUT."
		assert "country"        in self.INPUT, "cannot find 'country' in INPUT."
		assert "name"           in self.INPUT, "cannot find 'name' in INPUT."
		assert "category"       in self.INPUT, "cannot find 'category' in INPUT."

		self.driver.get("https://www.picodash.com/")

		btn_login = self.driver.find_element_by_xpath('//*[@id="infobar"]/div[2]/a[1]')
		btn_login.click()

		self.wait.until(lambda driver:driver.find_element_by_xpath('//*[@id="login-form"]/p[3]/input'))
		txt_username = self.driver.find_element_by_xpath('//*[@id="id_username"]')
		txt_password = self.driver.find_element_by_xpath('//*[@id="id_password"]')
		btn_login    = self.driver.find_element_by_xpath('//*[@id="login-form"]/p[3]/input')

		txt_username.send_keys(self.ig_username)
		txt_password.send_keys(self.ig_password)
		btn_login.click()

		self.wait.until(lambda driver:driver.find_element_by_xpath('//*[@id="activeinfo"]/div[3]/a'))
		lat = self.INPUT["lat"]
		lon = self.INPUT["long"]
		url = "https://www.picodash.com/explore/locations?location={lat}%20{lon}".format(
			lat = lat,
			lon = lon
		)
		self.driver.get(url)

		self.wait.until(lambda driver:driver.find_element_by_xpath("//div[@class='grid-cell']"))
		locations      = self.driver.find_elements_by_xpath("//div[@class='grid-cell']")
		location_links = list()
		location_names = list()
		for location in locations:
			location_name = location.text
			location_name = location_name.replace("\n","")
			location_link = location.find_element_by_xpath(".//a")
			location_link = location_link.get_attribute("href")
			location_links.append(location_link)
			location_names.append(location_name)

		for link in location_links:
			self.driver.get(link)

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

			media  = self.driver.find_element_by_xpath("//div[@id='media']")
			photos = media.find_elements_by_class_name("grid-cell")
			for media in photos:
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
						               Track = self.INPUT["track"],
						                City = self.INPUT["city"].strip(),
						             Country = self.INPUT["country"],
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
							    name = self.INPUT["name"],
							     lat = self.INPUT["lat"],
							    long = self.INPUT["long"],
							category = self.INPUT["category"],
							   track = self.INPUT["track"]	
						),
						    PostCreated_Time = "{}-{}-{}".format(published_date.year, str(published_date.month).zfill(2), str(published_date.day).zfill(2)),
						   PostInserted_Date = "{}-{}-{}".format(arrow.now().year, str(arrow.now().month).zfill(2), str(arrow.now().day).zfill(2)),
						          PostSource = "INSTAGRAM"
					)
					# print(bson.json_util.dumps(media, indent=4, separators=(",",":")))
					callback(media=media)
					btn_close.click()
				except ValueError:
					print("[picodash_crawler] Something wrong!")
				except selenium.common.exceptions.ElementNotVisibleExceptions:
					print("[picodash_crawler] Something wrong!")
			#end for
		#end for
	#end def
#end class