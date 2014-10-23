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
			 'Housing_Units[Very_Low_Income]',
			 'Housing_Units[Low_Income]',
			 'Housing_Units[Moderate_Income]',
			 'Housing_Units[Middle_Income]',
			 'Housing_Units[High_Income]',
			# 'total_expenditures', # <-- this one didn't work!
			 ]
steps = 2 #1600	# number of time steps #this doesn't seem to matter


#what do the graphs look like?
xlabel = 'years'


def request():
	"""
	Returns a JSON containing the sliders and buttons that the
	model wants.	Goes through the list of inputs and builds the
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
	
def work(args):
  """
  Run the model with the supplied data: *data* should be a list
  of values corresponding to each input parameter.
  """
  try:
    #print "HERE 0"
    #convert data
    data = {}
    for d in range(0,len(args),2):
      data[inputs[d/2]['entity']] = args[d+1]#DEBUG with fake values
      #data[args[d]] = args[d+1]
    if len(data) != len(inputs): # only except one value per parameter
      raise ValueError, "need to supply exactly "+str(len(inputs))+" inputs. Got "+str(len(data))
	
		#initialize the model
    #print "HERE 1"
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    query = host+model+'&command=init'
    response = opener.open(query)
    read = response.read()
    dictionary = json.loads(read)
    if not dictionary['success']:
      raise Exception, dictionary+" : in INITIALIZE"
			
		#pass the input values
    query = host+model+"&command=currentInputValue&inputs="
    query+= str([{"entity":input_['entity'], "currentValue":data[input_['entity']], "isGraphicalFunction":False} for input_ in inputs])
    query = query.replace('False','false') # change capitaliation
    query = query.replace(" ","")
    response = opener.open(query)
    read = response.read()
    dictionary = json.loads(read)
    if not dictionary['success']:
      raise Exception, dictionary	+" : in PASSING INPUT"
		
		#run for a number of timesteps
    for s in range(steps):
      query = host+model+'&command=run'
      response = opener.open(query)
      read = response.read()
      dictionary = json.loads(read)
      if not dictionary['success']:
        raise Exception, dictionary+" : in RUN"
				
		#grab the output and place
    query = host+model+'&command=currentOutputValue&outputs='
    query+= str(outputs)
    query+='&lastSampleIndex=-1'
    query = query.replace(" ","")
    response = opener.open(query)
    read = response.read()
    dictionary = json.loads(read)
    if not dictionary['success']:
      raise Exception, dictionary+" : in GRAB OUTPUT"
    
    #build graphs
    #print "HERE 2"
    responses = json.loads(dictionary['response'])
    graphs = []
    #print "HERE 2.1"
    graphs.append(make_housing_graph(responses))
    #print "HERE 2.2"
    graphs.append(make_revenue_graph(responses))

    #stop the simulation
    #print "HERE 3"
    query = host+model+'&command=stop'
    response = opener.open(query)
    read = response.read()
    dictionary = json.loads(read)
    if not dictionary['success']:
      raise Exception, dictionary+" : in STOP"

    #finish
    #print "FINISH", graphs
    return json.dumps(graphs)
  except Exception as e:
    raise e
    return json.dumps({
                'success':False,
                'error':str(e)
			     })

def make_housing_graph(responses):
  #set attributes of the graph
  graph = {  "name": "HousingUnits", 
        "type": "serial",
        "pathToImages": "http://cdn.amcharts.com/lib/3/images/",
        "categoryField": "category",
        "startDuration": 1,
        "categoryAxis": {
          "gridPosition": "start"
        },
        "trendLines": [],
        "guides": [],
        "valueAxes": [
          {
            "id": "ValueAxis-1",
            "title": "Number of Housing Units"
          }
        ],
        "allLabels": [],
        "balloon": {},
        "legend": {
          "useGraphSettings": True
        },
        "titles": [
          {
            "id": "HousingUnits",
            "size": 15,
            "text": "Number of Housing Units"
          }
        ]}

  #add various graphs
  graph["graphs"] = []
  for response in responses:
    response = json.loads(response)

    #skip the debt and total taxes graph
    if response['entity'] in ['debt', 'total_taxes']:
      continue

    #add a graph
    #print "  adding graph from", response['entity']
    graph["graphs"].append(
          {
            "balloonText": "[[title]] = [[value]]",
            "bullet": "round",
            "id": "AmGraph-1",
            "title": response["entity"],
            "type": "smoothedLine",
            "valueField": response["entity"]
          }
        )
  #print 
  #add data for the graph
  scale = 100  # only grab this many
  graph["dataProvider"] = []
  for x in range(0, len(response['values']), scale):
    graph["dataProvider"].append({"category": x})
    for response in responses:
      response = json.loads(response)
      #skip the debt and total taxes graph
      if response['entity'] in ['debt', 'total_taxes']:
        continue
      #print "  adding data for", x,"from", response['entity']
      #response['values'] = response['values'][::scale]  # limit number of data points
      graph["dataProvider"][-1][response["entity"]] = response["values"][x]

  return graph

def make_revenue_graph(responses):
  #set attributes of the graph
  graph = {  "name": "Financials", 
        "type": "serial",
        "pathToImages": "http://cdn.amcharts.com/lib/3/images/",
        "categoryField": "category",
        "startDuration": 1,
        "categoryAxis": {
          "gridPosition": "start"
        },
        "trendLines": [],
        "guides": [],
        "valueAxes": [
          {
            "id": "ValueAxis-1",
            "title": "Amount in Dollars"
          }
        ],
        "allLabels": [],
        "balloon": {},
        "legend": {
          "useGraphSettings": True
        },
        "titles": [
          {
            "id": "Financials",
            "size": 15,
            "text": "Financials"
          }
        ]}

  #add various graphs
  graph["graphs"] = []
  for response in responses:
    response = json.loads(response)

    #skip the non- debt and total taxes graph
    if response['entity'] not in ['debt', 'total_taxes']:
      continue

    #add a graph
    graph["graphs"].append(
          {
            "balloonText": "[[title]] = [[value]]",
            "bullet": "round",
            "id": "AmGraph-1",
            "title": response["entity"],
            "type": "smoothedLine",
            "valueField": response["entity"]
          }
        )
    response['values'] = response['values'][::100]  # limit number of data points

  #add data for the graph
  scale = 100  # only grab this many
  graph["dataProvider"] = []
  for x in range(0, len(response['values']), scale):
    graph["dataProvider"].append({"category": x})
    for response in responses:
      response = json.loads(response)
      #skip the non- debt and total taxes graph
      if response['entity'] not in ['debt', 'total_taxes']:
        continue
      #response['values'] = response['values'][::scale]  # limit number of data points
      graph["dataProvider"][-1][response["entity"]] = response["values"][x]

  return graph

#SCRIPT STARTS HERE#
try:
	action = sys.argv[1]		 
	if action == 'request':
		print request()
	elif action == 'work':
		print work(sys.argv[2:])
	else:
		json.dumps({
			'success':False,
			'error': 'Unknown action:{0}'.format(action)
			})
except IndexError:
	json.dumps({"success":False})
