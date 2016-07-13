from lib.location_data import LocationData
from tqdm              import tqdm
import bson.json_util

location_data  = LocationData()
locations      = location_data.get_locations(all=True)
total_location = len(locations)

locations      = tqdm(locations)
locations.set_description("[test][debug] Set as idle...")
for location in locations:
	location_data.set_as_idle(location)
locations = [l for l in location_data.get_locations(all=True) if "idle" not in l["status"]]
assert len(locations) == 0, "[test][error] total_location is not equalt to len(locations)"
print("[test][pass] Idle Test")

locations = location_data.get_locations(all=True)
locations = tqdm(locations)
locations.set_description("[test][debug] Set as processing...")
for location in locations:
	location_data.set_as_processing(location)
locations = [l for l in location_data.get_locations(all=True) if "processing" not in l["status"]]
assert len(locations) == 0, "[test][error] Not all location in processing status"
print("[test][pass] Processing Test")

locations = location_data.get_locations(all=True)
locations = tqdm(locations)
locations.set_description("[test][debug] Set as processed...")
for location in locations:
	location_data.set_as_processed(location)
locations = [l for l in location_data.get_locations(all=True) if "processed" not in l["status"]]
assert len(locations) == 0, "[test][error] Not all location in processed status"
print("[test][pass] Processed Test")

locations = location_data.get_locations()
print("[test][debug] Rolling back...")
locations = [l for l in location_data.get_locations(all=True) if "idle" not in l["status"]]
assert len(locations) == 0, "[test][error] Failed to rollback"
print("[test][pass] Rollback Test") 