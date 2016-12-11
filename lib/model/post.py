from .location import Location

class Post:
	def __init__(self, **kwargs):
		self.track 					  = kwargs.get("track", None)
		self.city  					  = kwargs.get("city", None)
		self.country 				  = kwargs.get("country", None)
		self.post_caption_text 		  = kwargs.get("post_caption_text", None)
		self.post_id  		   		  = kwargs.get("post_id", None)
		self.post_std_res_picture_url = kwargs.get("post_std_res_picture_url", None)
		self.post_likes   			  = kwargs.get("post_likes", None)
		self.post_url 				  = kwargs.get("post_url", None)
		self.post_geolocation		  = kwargs.get("post_geolocation", Location())
		self.post_tags 				  = kwargs.get("post_tags", None)
		self.post_type				  = kwargs.get("post_type", "image")
		self.post_from_user_id        = kwargs.get("post_from_user_id", None)
		self.post_from_username 	  = kwargs.get("post_from_username", None)
		self.post_user_profile_pic    = kwargs.get("post_user_profile_pic", None)
		self.query_search_location    = kwargs.get("query_search_location", Location())
		self.post_created_time  	  = kwargs.get("post_created_time", None)
		self.post_inserted_date       = kwargs.get("post_inserted_date", None)
		self.post_inserted_date_iso   = kwargs.get("post_inserted_date_iso", None)
		self.post_source              = kwargs.get("post_source", "INSTAGRAM")

	def to_dict(self):
		return {
			"Track": self.track,
			"City": self.city,
			"Country": self.country,
			"PostCaptionText": self.post_caption_text,
			"PostId": self.post_id,
			"PostStdResPictureUrl": self.post_std_res_picture_url,
			"PostLikes": self.post_likes,
			"PostUrl": self.post_url,
			"PostGeolocation": {
				"latitude": self.post_geolocation.lat,
				"longitude": self.post_geolocation.long,
				"name": self.post_geolocation.name,
				"id": self.post_geolocation.id
			},
			"PostTags": self.post_tags,
			"PostType": "image",
			"PostFromUserId": self.post_from_user_id,
			"PostFromUsername": self.post_from_username,
			"PostUserProfilePict": self.post_user_profile_pic,
			"QuerySearchLocation": {
				"name": self.query_search_location.name,
				"lat": self.query_search_location.lat,
				"long": self.query_search_location.long,
				"category": self.query_search_location.category,
				"track": self.query_search_location.track
			},
			"PostCreated_Time": self.post_created_time,
			"PostInserted_Date": self.post_inserted_date,
			"PostInserted_Date_ISO": self.post_inserted_date_iso,
			"PostSource": self.post_source
		}