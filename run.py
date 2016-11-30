from lib.logger 		 import Logger
from lib.engine.picodash import PicodashEngine

def execute_thread(data):
	location, cookies = data

	saver                  = SaverFactory.get_saver(SaverFactory.POST)
	engine 		           = PicodashEngine()
	engine.browser.cookies = cookies
	engine.browser.apply_cookies()
	engine.crawl(location, saver=saver)

if __name__ == "__main__":
	Logger()
	
	engine = PicodashEngine()
	engine.username = "amoure20"
	engine.password = "081703706966"

	engine.login()
	with multiprocessing.Pool(1) as pool:
		# Getting cookie from browser
		cookies = engine.browser.get_cookies()
		cookies = [cookie for cookie in cookies if "picodash" in cookie["domain"]]
		pool.map(execute_thread, [data, data])