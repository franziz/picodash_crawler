import time
import random

class BrowserTools(object):
	def __init__(self, webdriver=None):
		self.driver = webdriver

	def scroll(self, max_scroll=10):
		assert self.driver is not None, "driver is not defined."

		has_more  = True
		scrolled  = 0		
		while has_more:
			more  = self.driver.find_element_by_xpath("//div[@id='more']")
			style = more.get_attribute("style")
			if "display: none;" not in style and style and scrolled < max_scroll:
				scrolled = scrolled + 1
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight+10)")
				time.sleep(random.randint(100,500)/1000)
			else:
				has_more = False
		#end while
