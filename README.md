# Picodash Crawler
This crawler will require an input from JSON file. 

Sample Input
```json
{
	     "name":" autogenPointII 1",
	      "lat":"14.6526527",
	     "long":"120.881398",
	 "category":"blanketCover",
	    "track":"MakatiBlanket",
	     "city":"Makati",
	  "country":"Philippines",
	"processed":"FALSE",
	  "address":""
}
```

# Requirement
1. Python 3
2. arrow
3. pymongo
4. pytz
5. tzlocal
6. selenium

```bash
pip3 install arrow pymongo tzlocal pytz selenium
```

NOTE: Some of requirements maybe not listed. In order to run this properly, you might want to pull this application docker image.

```bash
docker pull franziz/picodash_crawler
docker run -it --name picodash_crawler franziz/picodash_crawler
```

# How to use
This git is an application level. There is not configuration file to customize this application. In order to use this application, just simply run 
```bash
python3 run.py
```

# Under the hood
the INPUT from the example is using MOCK_INPUT. You can change the INPUT depends on the requirement. However, the template is mentioned above.
```python
from engine import Engine
import bson.json_util

def callback(media=None):
	assert media is not None, "media is not defined."
	print(bson.json_util.dumps(media, indent=4, separators=(",",":")))

engine             = Engine(driver=Engine.CHROME)
engine.INPUT       = MOCK_INPUT
engine.ig_username = "xzerocool"
engine.ig_password = "isidsea"
engine.crawl(callback)
```