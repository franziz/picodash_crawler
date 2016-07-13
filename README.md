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

# Simple Usage
Setting up config file. The default config file is located at `/root/app/config.json`. If you are using picodash_crawler image, you need to make config file from there.
```json
{
	"ig":{
		"username":"xxx",
		"password":"xxx"
	}
}
```

Because picodash.login() will save the cookies and close the browser, you need to make a new instance of `Picodash()`. This new Instance has a new ability to crawl the website.
```python
	picodash = Picodash()
	picodash.login()

	new_instance         = Picodash()
	new_instance.cookies = picodash.cookies
	new_instance.apply_cookies()
	new_instance.crawl(location_data=MOCK_INPUT, callback=callback)	
```