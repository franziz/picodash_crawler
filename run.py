from selenium.common.exceptions import WebDriverException
from lib.logger 		 		import Logger
from lib.engine.picodash 		import PicodashEngine
from lib.factory.finder  		import FinderFactory
from lib.factory.saver   		import SaverFactory
from lib.factory.config			import ConfigFactory
from lib.model.proxy     		import Proxy
import multiprocessing
import click
import arrow
import shutil
import os

def execute_thread(data):
	location, cookies, start, end, proxy = data
	location.set_as_processing()

	saver  = SaverFactory.get_saver(SaverFactory.POST)
	engine = PicodashEngine(proxy=proxy)

	engine.browser.get("https://www.picodash.com/")
	engine.browser.cookies = cookies
	engine.browser.apply_cookies()

	try:
		engine.crawl(location, saver=saver, start_date=start, end_date=end)
	except WebDriverException as ex:
		engine.browser.driver.save_screenshot(os.path.join(os.getcwd(),"screenshot", "error.jpg"))
		print("[error] %s" % ex)
	engine.browser.close()
	location.set_as_processed()

@click.command()
@click.option("--start", default=arrow.now().timestamp, help="Crawling Start Date [yyyy/mm/dd]", type=str)
@click.option("--end", default=arrow.now().timestamp, help="Crawling End Date [yyyy/mm/dd]", type=str)
@click.option("--workers", default=1, help="Crawler workers. default = 1")
@click.option("--noproxy", default=True, help="true or false", type=bool)
def main(start, end, workers, noproxy):
	# clear
	shutil.rmtree(os.path.join(os.getcwd(),"screenshot"))
	os.mkdir(os.path.join(os.getcwd(),"screenshot"))

	start = arrow.get(start).floor("day").timestamp
	end   = arrow.get(end).ceil("day").timestamp
	proxy = None if noproxy else Proxy()

	config = ConfigFactory.get_config(ConfigFactory.LOGIN)
	config = config.get("login")

	engine          = PicodashEngine(proxy=proxy)
	engine.username = config["username"]
	engine.password = config["password"]

	engine.login()
	with multiprocessing.Pool(workers) as pool:
		# Getting cookie from browser
		cookies = engine.browser.get_cookies()
		cookies = [cookie for cookie in cookies if "picodash" in cookie["domain"]]
		engine.browser.close()

		# Get locations from database 
		finder    = FinderFactory.get_finder(FinderFactory.LOCATION)
		locations = finder.find()
		data 	  = [(location, cookies, start, end, proxy, ) for location in locations]
		
		pool.map(execute_thread, data)

if __name__ == "__main__":
	# Logger()
	main()