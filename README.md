# Picodash Crawler

Picodash Crawler is a simple crawler made with love with Picodash. The main purpose of this crawler is to grab every instagram data from Picodash to your local database. If you are interested with this project, please feel free to contribute to this project.
> <b>NOTE:</b> 
> You need a Picodash valid subscription in order to run this application.
> This is not a library. This is an application that run based on configuration.

### Instalation
Config needed in order to run without error:

 - database.json (Store database location)
 - login.json (Store login information including username and password)
 - proxy.json (Store proxy database location)
 - sentry.json (Store Sentry public and secret key)

> Keep scrolling down to find all configuration details.

In order to install Picodash crawler, you need to:

 - `docker pull franziz/picodash-crawler:phantomjs`
 - `git clone http://github.com/franziz/picodash_crawler`
 - `cd picodash_crawler`
 - `mkdir config`
 - `cd config`
 - Make every configuration inside config folder.
 - `cd ..` to exit from config folder
 - `docker run -it --name picodash-crawler -v $(pwd):/root/app -w /root/app franziz/picodash-crawler:phantomjs python run.py`

### Arguments
There are several arguments accepted by run.py:

 - `--start`: Crawling start date [yyyy/mm/dd]
 - `--end`: Crawling end date [yyyy/mm/dd]
 - `--workers`: Crawler workers. default = 1
 - `--noproxy` true or false

#### database.json
```json
{
	"postSaver":{
		"connectionString": "xxx",
		"collection": "xxx",
		"database": "xxx"
	}
}
```
Please make sure that you have correct `connectionString` parameter.

#### login.json
```json
{
	"login":{
		"username": "xxx",
		"password": "xxx"
	}
}
```
You need a valid Instagram account that has been linked to Picodash. 

#### proxy.json
```json
{
	"proxy":{
		"ip": "xxx",
		"port": xxx,
		"database": "xxx",
		"collection": "xxx"
	}
}
```

#### sentry.json
```json
{
	"sentry":{
		"ip": "xxx",
		"port": xxx,
		"public_key": "xxx",
		"secret_key": "xxx",
		"project_id": xxx
	}
}
```

