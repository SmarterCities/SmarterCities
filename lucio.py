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
    return json.dumps([{"data_name":"311",
                            "sliders":[{"keys":["agency_name"],
                                        "values":["NYPD"],
                                        "function":"count",
                                        "min":0,
                                        "max":20,
                                        "name":"NYPD calls"}],
                            "buttons":[]
                        }])
    
def work(data):
    """
    Run the model with the supplied data. This simple models
    assumes call volume will increase linearly for the next
    10 weeks.
    """
    try:
        x = float(data)
        graph = {"values":{str(t):str(x*t) for t in range(10)}}
        graph["title"] = "Projected 311 calls to NYPD"
        return json.dumps([graph])
    except ValueError:
        print 'data provided not a float'


action = sys.argv[1]         
if action == 'request':
    print request()
elif action == 'work':
    print work(sys.argv[2])
else:
    print 'Unknown action provided:',action
