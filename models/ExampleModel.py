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
    #If I want the Framework to make API calls I need to supply
    #a JSON object like this one:
#    return json.dumps({"sliders":[{"data":"311", 
#                                   "keys":["agency_name"],
#                                   "values":["NYPD"],
#                                   "process":"count",
#                                   "min":0,
#                                   "max":20,
#                                   "name":"NYPD calls"}, 
#                                  {"data":"311",
#                                   "keys":["agency_name"],
#                                   "values":["TLC"],
#                                   "process":"count",
#                                   "min":0,
#                                   "max":50,
#                                   "name":"TLC calls"}],
#                        "buttons":[] })
    
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
                        "buttons":[] })
    
def work(data):
    """
    Run the model with the supplied data. This simple models
    assumes call volume will increase linearly for the next
    10 weeks.
    """
    try:
        if len(data) != 5:
            raise Exception, data
        
        data = map(float,data)
        slope = sum(data)
        
        #Tax Revenue
        graph1 = {}
        graph1["x"] = map(str, range(10))
        graph1["y"] = [str(slope*x) for x in range(10)]
        graph1["title"] = ''
        graph1["xlabel"] = ''
        graph1["ylabel"] = ''
        
        #Cost of services
        graph2 = {}
        graph2["x"] = map(str, range(10))
        graph2["y"] = [str((-slope*x)+slope) for x in range(10)]
        graph2["title"] = ''
        graph2["xlabel"] = ''
        graph2["ylabel"] = ''
        
        #Amount of Debt
        graph3 = {}
        graph3["x"] = map(str, range(10))
        graph3["y"] = [str(x+slope) for x in range(10)]
        graph3["title"] = 'Effects'
        graph3["xlabel"] = 'Years'
        graph3["ylabel"] = 'Dollars'        
        
        return json.dumps([graph1, graph2, graph3])
    except ValueError:
        print 'data provided not a float'

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
