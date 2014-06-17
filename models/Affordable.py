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
model = 'simID=netsim/pharmacokinetics'

inputs = [{'entity':'dosage',
           'currentValue':0, # default value
           'min':0,
           'max':2000}]

outputs = ['blood__concentration','toxic_concentration']
steps = 10  # number of time steps

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
                       "buttons":[] })
    
def work(data):
    """
    Run the model with the supplied data: *data* should be a list
    of values corresponding to each input parameter.
    """
    try:
        if len(data) > len(inputs): # only except one value per parameter
            raise Exception, data
            
        data = map(int,map(float,data))  # convert strings to floats
        
        #initialize the model
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        query = host+model+'&command=init'
        response = opener.open(query)
        read = response.read()
        dictionary = json.loads(read)
        if not dictionary['success']:
            raise Exception, dictionary
            
        #DEBUG
        #print "===init==="
        #print 'query',query
        #print 'dictionary',dictionary
        #print 
            
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
            
        #DEBUG
        #print "===set inputs==="
        #print 'query',query
        #print 'dictionary',dictionary
        #print
        
        #run for a number of timesteps
        for s in range(steps):
            query = host+model+'&command=run'
            response = opener.open(query)            
            read = response.read()
            dictionary = json.loads(read)
            if not dictionary['success']:
                raise Exception, dictionary
                
        #DEBUG
        #print "===run",steps,"times==="
        #print 'query',query
        #print 'dictionary',dictionary
        #print
        
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
            
        #DEBUG
        #print "===grab outputs==="
        #print 'query',query
        #print 'dictionary',dictionary
        #print
        
        #build graphs
        graphs = []
        responses = json.loads(dictionary['response'])
        for response in responses:
            response = json.loads(response)
            #print "response = ",response,"type",type(response)
            
            graph = {}
            graph['title']=response["entity"]
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
            
        #DEBUG
        #print "===send stop==="
        #print 'query',query
        #print 'dictionary',dictionary
        #print
        
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
