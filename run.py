from lib.logger 		 import Logger
from lib.engine.picodash import PicodashEngine
from lib.factory.finder  import FinderFactory
from lib.factory.saver   import SaverFactory
import multiprocessing
import click
import arrow

def execute_thread(data):
	location, cookies = data

	saver  = SaverFactory.get_saver(SaverFactory.POST)
	engine = PicodashEngine()

	engine.browser.get("https://www.picodash.com/")
	engine.browser.cookies = cookies
	engine.browser.apply_cookies()
	engine.crawl(location, saver=saver)

@click.command()
@click.option("--start", default=None, help="Crawling Start Date [yyyy/mm/dd]")
@click.option("--end", default=None, help="Crawling End Date [yyyy/mm/dd]")
@click.option("--workers", default=1, help="Crawler workers. default = 1")
def main(start, end, workers):
	start = arrow.get(start) if start is not None else arrow.utcnow().timestamp
	end   = arrow.get(end) if end is not None else arrow.utcnow().timestamp

	engine = PicodashEngine(proxy=None)
	engine.username = "amoure20"
	engine.password = "081703706966"

	engine.login()
	with multiprocessing.Pool(workers) as pool:
		# Getting cookie from browser
		cookies = engine.browser.get_cookies()
		cookies = [cookie for cookie in cookies if "picodash" in cookie["domain"]]
		engine.browser.close()

		# Get locations from database 
		finder    = FinderFactory.get_finder(FinderFactory.LOCATION)
		locations = finder.find()
		data 	  = [(location, cookies,) for location in locations]
		
		pool.map(execute_thread, data)

if __name__ == "__main__":
	Logger()
	main()