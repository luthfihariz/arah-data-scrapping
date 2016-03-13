import sys
import json, requests
from pprint import pprint
from datetime import datetime
from dbconfig import db

SOURCE_NAME = "Angkot.web.id"
ANGKOT_WEB_ID_URL = "https://angkot.web.id/route/transportation/{}.json"

def main():
	for id in range(1,1000):
		route = parse_response_to_route(ANGKOT_WEB_ID_URL.format(id), id)
		if route:
			try:
				db['public_transport_route'].insert(route)
				print("ID {} new route inserted: {} from {}".format(id, route['source']['id'], route['source']['name']))
			except:
				print("ID {} Failed to insert".format(id))


def parse_response_to_route(url, id):
	result = get_json_from_url(url)
	if result['status'] == "ok":
		submission_id = result['submission_id']
		if submission_id:
			previous_routes = db['public_transport_route'].find_one({'source.id':submission_id})
			if previous_routes and previous_routes['source']['name'] == SOURCE_NAME:
				print("ID {} Submission id : {} already exist in database.".format(id, submission_id))
			else:
				print("ID {} Inserting new route : {}".format(id,submission_id))
				geojson = result['geojson']
				geojson_properties = geojson['properties']
				route = {
					"source" : {
						"name" : SOURCE_NAME,
						"id" : submission_id
					},
					"province" : geojson_properties['province'],
					"city" : geojson_properties['city'],
					"company" : geojson_properties['company'],
					"number" : geojson_properties['number'],
					"origin" : geojson_properties['origin'],
					"destination" : geojson_properties['destination'],
					"geometry" : geojson['geometry'],
					"updated" : str(datetime.now()),
					"created" : str(datetime.now())
				}
				return route
		else:
			print("ID {} doesnt have submission id. Skipped.".format(str(id)))
	else:
		print("ID {} api failed".format(str(id)))

			
def get_json_from_url(url):
	response = requests.get(url=url)
	data = json.loads(response.text)
	return data


if __name__ == '__main__':
	sys.exit(main())