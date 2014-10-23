"""
Created on Sun May 18 08:34:11 2014

@author: Lucio

This is the example BOB for using the frame. It is a simple
model that tries to predict the number of 311 calls with
the agency name is NYPD. 
"""

import sys
import json

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
                                   "max":100,
                                   "name":"AMI 1",
                                   "value":10},
                                  {"min":0,
                                   "max":100,
                                   "name":"AMI 2",
                                   "value":15},
                                  {"min":0,
                                   "max":100,
                                   "name":"AMI 3",
                                   "value":15},
                                   {"min":0,
                                   "max":100,
                                   "name":"AMI 4",
                                   "value":15},
                                   {"min":0,
                                   "max":100,
                                   "name":"AMI 5",
                                   "value":15},
                                   ],
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

	output = [{	"name": "ExampleChart", 
				"type": "serial",
				"pathToImages": "http://cdn.amcharts.com/lib/3/images/",
				"categoryField": "category",
				"startDuration": 1,
				"categoryAxis": {
					"gridPosition": "start"
				},
				"trendLines": [],
				"graphs": [
					{
						"balloonText": "Slider [[category]] is at [[value]]",
						"bullet": "round",
						"id": "AmGraph-1",
						"title": "Example Graph",
						"type": "smoothedLine",
						"valueField": "column-1"
					},
				],
				"guides": [],
				"valueAxes": [
					{
						"id": "ValueAxis-1",
						"title": "Slider Value"
					}
				],
				"allLabels": [],
				"balloon": {},
				"legend": {
					"useGraphSettings": True
				},
				"titles": [
					{
						"id": "Slider value",
						"size": 15,
						"text": "Slider Values"
					}
				]
		}]
	data_provider = [ { "category": "variable " + k,
					 "column-1":cleaned[k]} for k in cleaned]
	output[0]["dataProvider"] = data_provider
	return json.dumps(output)
		

#these are necessary for calling the Model from the command line
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
