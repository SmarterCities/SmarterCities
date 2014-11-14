"""
Created on Mon 11-10-14

@author: Lucio

Model for visualizing different pulses of the city.

"""

import sys
import json
import requests

def request():
    """
    Returns a JSON containing the options for visualizing city pulse.
    """
    return json.dumps({"dropdowns":[{"name":"Pulses", "values":["Craigs List", "MTA Turnstyle", "Citi Bike", "Traffic Speed"]}]})
    
def work(data):
	"""
	Build the map for the requested pulse option. 
	"""
	#verify input
	if data[0] != "Pulses" or data[1] not in ["Craigs List", "MTATurnstyle", "CitiBike", "TrafficSpeed"]:
		raise ValueError, "incorrent data returned:" + str(data)

	#build map based on pulse value
	if data[1] == "Craigs List":
		pass


	return json.dumps({"amCharts":[], "maps":[], "text": data})

#these are necessary for calling the Model from the command line
"""
Example work command:

python models/311Messages.py work Pulses CitiBike

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
