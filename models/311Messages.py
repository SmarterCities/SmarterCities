"""
Created on Sun May 18 08:34:11 2014

@author: Lucio

Model for getting 311 calls within a certain area.

"""

import sys
import json
import requests

def request():
    """
    Returns a JSON containing the sliders and buttons that the
    BOB wants.  Here we want a single slider that reflects the
    number of 311 calls with agent_name=NYPD. The framework 
    will make the API call for us.
    """    
    #If I know the values for the sliders / button a priori
    #then I can supply a JSON object like this:
    return json.dumps({"sliders":[{"min":0,
                                   "max":5000,
                                   "name":"Radius",
                                   "value":1000},
                                   ],
                        "entries":[{"name":"Latitude"},
                        		   {"name":"Longitude"}],
                        "buttons":[],
						"rectangles":[]})
    
def work(data):
	"""
	Run the model with the supplied data. This simple models
	assumes call volume will increase linearly for the next
	10 weeks.
	"""
	cleaned = {}
	for d in range(0,len(data),2):
		cleaned[data[d]] = data[d+1]

	#make an API call and build map items
	r = requests.get("http://data.cityofnewyork.us/resource/erm2-nwe9.json?created_date=2014-10-31T00:00:00&$where=within_circle(location,{0},{1},{2})".format(cleaned["Latitude"], cleaned["Longitude"], cleaned["Radius"]))
	map_ = {}
	map_["name"] = "311ServiceRequests"
	map_["view"] = {"lat":cleaned["Latitude"], "lon":cleaned["Longitude"], "zoom":13}
	map_["markers"] = [ {"lat":sr["latitude"], 
						 "lon":sr["longitude"],
						 "text":sr["complaint_type"]} for sr in r.json()]
	map_["circles"] = [ {"lat":cleaned["Latitude"], 
						 "lon":cleaned["Longitude"], 
						 "radius":cleaned["Radius"],
						 "color":"red",
						 "fillColor": '#f03',
				    	 "fillOpacity": 0.5} ]

	return json.dumps({"amCharts":[], "maps":[map_]})

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
