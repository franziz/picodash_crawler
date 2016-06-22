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

# How to use
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