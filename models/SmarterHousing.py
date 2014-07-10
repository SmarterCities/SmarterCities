"""
Created on Sat June 15 08:34:11 2014

@author: Lucio

This is a wrapper for a System Dynamics model hosted on forio.
The hosting address, inputs, outputs, minimum and maximum values
all must be defined a priori.

"""

import sys
import json
import urllib2
import cookielib

#define the model and how to use it
host = 'http://forio.com/service2/netsimruntime.ashx?'
model = 'simID=karimc17/simplesthousing'

inputs = [{'entity':'percent_by_income[Extremely_Low_Income]',
           'currentValue':16.66, # default value
           'min':0,
           'max':100},
		  {'entity':'percent_by_income[Very_Low_Income]',
           'currentValue':16.66, # default value
           'min':0,
           'max':100},
		  {'entity':'percent_by_income[Low_Income]',
           'currentValue':16.67, # default value
           'min':0,
           'max':100},
		  {'entity':'percent_by_income[Moderate_Income]',
           'currentValue':16.67, # default value
           'min':0,
           'max':100},
		  {'entity':'percent_by_income[Middle_Income]',
           'currentValue':16.67, # default value
           'min':0,
           'max':100},
		  {'entity':'percent_by_income[High_Income]',
           'currentValue':16.67, # default value
           'min':0,
           'max':100},
		  {'entity':'Housing_Units[Extremely_Low_Income]',
           'currentValue':1000, # default value
           'min':0,
           'max':10000},
		  {'entity':'Housing_Units[Very_Low_Income]',
           'currentValue':1000, # default value
           'min':0,
           'max':10000},
		  {'entity':'Housing_Units[Low_Income]',
           'currentValue':1000, # default value
           'min':0,
           'max':10000},
		  {'entity':'Housing_Units[Moderate_Income]',
           'currentValue':1000, # default value
           'min':0,
           'max':10000},
		  {'entity':'Housing_Units[Middle_Income]',
           'currentValue':1000, # default value
           'min':0,
           'max':10000},
		  {'entity':'Housing_Units[High_Income]',
           'currentValue':1000, # default value
           'min':0,
           'max':10000}]
		   
outputs = ['total_taxes',
           'debt',
           'Housing_Units[Extremely_Low_Income]',
           #'Housing_Units[Very_Low_Income]',
           #'Housing_Units[Low_Income]',
           #'Housing_Units[Moderate_Income]',
           #'Housing_Units[Middle_Income]',
           #'Housing_Units[High_Income]',
            # 'total_expenditures', # <-- this one didn't work!
           ]
steps = 2 #1600  # number of time steps


#what do the graphs look like?
xlabel = 'hours'
ylabel = 'blood concentration'


def request():
    """
    Returns a JSON containing the sliders and buttons that the
    model wants.  Goes through the list of inputs and builds the
    JSON object.
    """
    return json.dumps({"sliders":[{'name':i['entity'],
                                   'min':i['min'],
                                   'max':i['max'],
                                   'value':i['currentValue']} for i in inputs],
                       "buttons":[],
                       "rectangles":[{"upper_left":[40.795296, -73.968362],
                                      "lower_right":[40.80, -73.97]}],
                                      "color":"blue" })
    
def work(data):
    """
    Run the model with the supplied data: *data* should be a list
    of values corresponding to each input parameter.
    """
    try:
        if len(data) != len(inputs): # only except one value per parameter
            raise Exception, "need to supply exactly "+str(len(inputs))+" inputs"
            
        data = map(int,map(float,data))  # convert strings to floats to ints
        
        #initialize the model
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        query = host+model+'&command=init'
        response = opener.open(query)
        read = response.read()
        dictionary = json.loads(read)
        if not dictionary['success']:
            raise Exception, dictionary
            
        #pass the input values
        query = host+model+"&command=currentInputValue&inputs="
        query+= str([{"entity":input_['entity'], "currentValue":data[index], "isGraphicalFunction":False} for index, input_ in enumerate(inputs)])
        query = query.replace('False','false') # change capitaliation
        query = query.replace(" ","")
        response = opener.open(query)        
        read = response.read()
        dictionary = json.loads(read)
        if not dictionary['success']:
            raise Exception, dictionary   
        
        #run for a number of timesteps
        for s in range(steps):
            query = host+model+'&command=run'
            response = opener.open(query)            
            read = response.read()
            dictionary = json.loads(read)
            if not dictionary['success']:
                raise Exception, dictionary
                
        #grab the output and place
        query = host+model+'&command=currentOutputValue&outputs='
        query+= str(outputs)
        query+='&lastSampleIndex=-1'
        query = query.replace(" ","")
        response = opener.open(query)        
        read = response.read()
        dictionary = json.loads(read)
        if not dictionary['success']:
            raise Exception, dictionary
             
        #build graphs
        graphs = []
        responses = json.loads(dictionary['response'])
        for response in responses:
            response = json.loads(response)
            #print "response = ",response,"type",type(response)
            
            graph = {}
            graph['title']=response["entity"]
            response['values'] = response['values'][::100]
            graph['x']=range(len(response['values']))
            graph['y']=response['values']
            graph['xlabel'] = xlabel
            graph['ylabel'] = ylabel
            graphs.append(graph)
        
        #stop the simulation
        query = host+model+'&command=stop'
        response = opener.open(query)        
        read = response.read()
        dictionary = json.loads(read)
        if not dictionary['success']:
            raise Exception, dictionary
        
        return json.dumps(graphs)
    except ValueError:
        return 'data provided not a float:',data
    except urllib2.HTTPError:
        return 'HTTP Error: query = '+query

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
