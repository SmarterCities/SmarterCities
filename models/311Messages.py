"""
Created on Thur November 13 08:34:11 2014

@author: Lucio

Model for getting 311 calls within a certain area.

"""

import sys
import json
import requests
import time
import numpy as np

def request():
    """
    Returns the necessary inputs in a JSON -- for this
    model there is not input so simply return a label.
    """    
    return json.dumps({"sliders":[],
                       "entries":[],
                       "buttons":[],
					 "rectangles":[],
					 "labels":["No input parameters -- just press run!"]})
    
def work(data):
	"""
	For each zip code, return a circle with epidemic intensity and 
	a marker for the request type.
	"""
	#1. Build data set
	days = [time.strftime("%Y-%m-%dT00:00:00", time.localtime(time.time() - (24*60*60*d))) for d in range(2,9)]
	data = {}
	for index, day in enumerate(days):
		r = requests.get("http://data.cityofnewyork.us/resource/erm2-nwe9.json?created_date={0}".format(day))
		for service_request in r.json():
			#1.1 grab relevant data
			try:
				zip_code = service_request["incident_zip"]
				incident_type = service_request["complaint_type"]
			except KeyError:
				#No incident zip or complaint type provided -- must be skipped
				continue

			#1.2 add zip if we haven't seen it yet
			if zip_code not in data:
				data[zip_code] = {}
				data[zip_code]["incidents"] = {}
				data[zip_code]["lat"] = float(service_request["latitude"])
				data[zip_code]["lon"] = float(service_request["longitude"])

			#1.3 add incident if doesn't exist
			if incident_type not in data[zip_code]["incidents"]:
				data[zip_code]["incidents"][incident_type] = {i:0 for i in range(7)}
			
			#1.4 tally incident type
			data[zip_code]["incidents"][incident_type][index]+=1

	#2. Analyze data for increasing request
	for zip_code in data:
		data[zip_code]["incident"] = None
		data[zip_code]["value"] = -np.inf
		for incident_type in data[zip_code]["incidents"]:
			x = range(7) 
			y = [data[zip_code]["incidents"][incident_type][d] for d in range(7)]
			slope, intercept = np.polyfit(x,y,1)  # fit a line to data

			if slope > data[zip_code]["value"]:
				data[zip_code]["value"] = slope
				data[zip_code]["incident"] = incident_type

	#3. Build maps from data
	map_ = {}
	map_["name"] = "311ServiceRequests"
	map_["view"] = {"lat":40.750254, "lon":-73.987339, "zoom":13}
	map_["circles"] = []
	map_["markers"] = []
	for zip_code in data:
		map_["circles"].append({"lat":data[zip_code]["lat"], 
				 				"lon":data[zip_code]["lon"], 
								"radius":500,
								"color":["blue","red"][data[zip_code]["value"]>1.0],
								"fillColor": ["blue","red"][data[zip_code]["value"]>1.0],
								"fillOpacity": 0.5})
		map_["markers"].append({"lat":data[zip_code]["lat"], 
								 "lon":data[zip_code]["lon"],
								 "text":data[zip_code]["incident"]+"\n"+str(data[zip_code]["value"])})

	return json.dumps({"maps":[map_]})

#these are necessary for calling the Model from the command line
"""
Example work command:

python models/311Messages.py work Latitude 40.752 Longitude -73.981 Radius 1000

"""
try:
    action = sys.argv[1]         
    if action == 'request':
        print request()
    elif action == 'work':
        print work(sys.argv[2:])
    else:
        print 'Unknown action provided:',action
except IndexError:
    json.dumps({"error":"True"})
