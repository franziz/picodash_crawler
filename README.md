# Picodash Crawler

Picodash Crawler is a simple crawler made with love with Picodash. The main purpose of this crawler is to grab every instagram data from Picodash to your local database. If you are interested with this project, please feel free to contribute to this project.
> <b>NOTE:</b> 
> You need a Picodash valid subscription in order to run this application.
> This is not a library. This is an application that run based on configuration.

## Instalation
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
 - `git remote update`
 - `git checkout new-logic`
 - `mkdir config`
 - `cd config`
 - Make every configuration inside config folder.
 - `cd ..` to exit from config folder
 - `docker run -it --name picodash-crawler -v $(pwd):/root/app -w /root/app franziz/picodash-crawler:phantomjs python3 run.py`

## Arguments
There are several arguments accepted by run.py:

 - `--start`: Crawling start date [yyyy/mm/dd]
 - `--end`: Crawling end date [yyyy/mm/dd]
 - `--workers`: Crawler workers. default = 1
 - `--noproxy` true or false

## Data Structure
### Input
Input is a location provided to IGFollowers application to crawl. 

| Key          | Types    | Description 									  |
|--------------|----------|---------------------------------------------------|
| _id 		   | ObjectId |   												  |
| address      | String   |    												  |
| category     | String   |    												  |
| city         | String   | City where the location belongs to 				  |
| country      | String   | Country where the location belongs to             |
| is_active    | Boolean  | Set it `false` if you do not want to include this |
| lat          | String   | Latitude of the location                          |
| long         | String   | Longitude of the location                         |
| name         | String   | Location name                                     |
| nextLatestId | String   | I do not know about this                          |
| processed    | Boolean  |                                                   |
| status       | String   | `processed`, `processing`, or `idle`              |
| track        | String   | Track ID							      	 	  |

### Output
Output data are saved based on `database.json` configuration file under `postSaver`field.

| Key                          | Types    | Description 						  |
|------------------------------|----------|---------------------------------------|
| _id                          | ObjectId | 									  |
| City                         | String   | City where the location belongs to    |
| Country                      | String   | Country where the location belongs to |
| PostCaptionText              | String   | A text from the post caption 		  |
| PostCreated_Time             | String   |  									  |
| PostFromUserId               | String   |  									  |
| PostFromUsername             | String   |                                       |
| PostGeolocation              | Object   | Detail of the location                |
| PostGeolocation.id           | Number   | Instagram ID of the location          |
| PostGeolocation.latitude     | Number   | Latitude of the location              |
| PostGeolocation.longitude    | Number   | Longitude of the location             | 
| PostGeolocation.name         | String   | Name of the location                  |
| PostId                       | String   | Usually a post ID from Instagram      |  
| PostInserted_Date            | String   | DD-MM-YYYY HH:MM                      |
| PostInserted_Date_ISO        | Date     | Just ISO format of the inserted date  |
| PostLikes                    | Number   | Number of likes for each post         |
| PostSource                   | String   | INSTAGRAM                             |
| PostStdResPictureUrl         | String   | URL of standard resolution picture    |
| PostTags                     | Array    | Array of Hastags (#)                  |
| PostType                     | String   | image                                 |
| PostUrl                      | String   | A direct link to the post             |
| PostUserProfilePict          | String   | User profile picture URL              |
| QuerySearchLocation          | Object   | Detail about query of the location    |
| QuerySearchLocation.category | null     | Nothing here                          |
| QuerySearchLocation.lat      | String   | Latitude of the query                 |
| QuerySearchLocation.long     | String   | Longitude of the query                |
| QuerySearchLocation.name     | String   | Query name                            |
| QuerySearchLocation.track    | String   | Query track ID                        |
| Track                        | String   | Post track ID                         |

## Configuration Template

### database.json
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

### login.json
```json
{
	"login":{
		"username": "xxx",
		"password": "xxx"
	}
}
```
> **Note:**
> You need a valid Instagram account that has been linked to Picodash. 
> This configuration cannot have multiple account.

### proxy.json
This configuration need to point a MongoDB database that store all proxy information. 
```json
{
	"proxy":{
		"ip": "xxx",
		"port": 0,
		"database": "xxx",
		"collection": "xxx"
	}
}
```

### sentry.json
```json
{
	"sentry":{
		"ip": "xxx",
		"port": 0,
		"public_key": "xxx",
		"secret_key": "xxx",
		"project_id": 0
	}
}
```

