"""
Created on Sun May 18 08:34:11 2014

@author: Lucio

This is the example BOB for using the frame. It is a simple
model that tries to predict the number of 311 calls with
the agency name is NYPD. 
"""

import sys
import json
from flask import jsonify

def request():
    """
    Returns a JSON containing the sliders and buttons that the
    BOB wants.  Here we want a single slider that reflects the
    number of 311 calls with agent_name=NYPD. The framework 
    will make the API call for us.
    """    
    #If I know the values for the sliders / button a priori
    #then I can supply a JSON object like this:
    return jsonify({"sliders":[{"min":0,
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
    return jsonify({
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
							"balloonText": "[[title]] of [[category]]:[[value]]",
							"bullet": "round",
							"id": "AmGraph-1",
							"title": "graph 1",
							"type": "smoothedLine",
							"valueField": "column-1"
						},
						{
							"balloonText": "[[title]] of [[category]]:[[value]]",
							"bullet": "square",
							"id": "AmGraph-2",
							"title": "graph 2",
							"type": "smoothedLine",
							"valueField": "column-2"
						}
					],
					"guides": [],
					"valueAxes": [
						{
							"id": "ValueAxis-1",
							"title": "Axis title"
						}
					],
					"allLabels": [],
					"balloon": {},
					"legend": {
						"useGraphSettings": true
					},
					"titles": [
						{
							"id": "Title-1",
							"size": 15,
							"text": "Chart Title"
						}
					],
					"dataProvider": [
						{
							"category": "category 1",
							"column-1": 8,
							"column-2": 5
						},
						{
							"category": "category 2",
							"column-1": "3",
							"column-2": 7
						},
						{
							"category": "category 3",
							"column-1": "0",
							"column-2": 3
						},
						{
							"category": "category 4",
							"column-1": 1,
							"column-2": 3
						},
						{
							"category": "category 5",
							"column-1": 2,
							"column-2": 1
						},
						{
							"category": "category 6",
							"column-1": 3,
							"column-2": 2
						},
						{
							"category": "category 7",
							"column-1": 6,
							"column-2": 8
						}
					]
				}
		)

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
