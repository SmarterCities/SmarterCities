"""
Framework is called by the web GUI. The web gui should
request to use a particular bob (supplied as argv[1]).

Example uses:

python Framework.py lucio input

python Framework.py lucio output 11

"""

import sys
import os
import json
import urllib2

def input_(model_file):
    #2. request data needs from bob
    model_response = os.popen('python {0} request'.format(model_file)).read().strip()
    inputs = json.loads(model_response)
    
    #3. Build objects dictionary for data
    objects = {}
    
    #3.1 build slider objects
    objects["sliders"] = []
    for slider in inputs["sliders"]:
        #build api query
        if "data" in slider:
            print "slider data", slider["data"]
            query = known_data_sets[slider["data"]]
            for i in range(len(slider["keys"])):
                query+=slider["keys"][i]+'='+slider["values"][i]+'&'
    
            #make query
            request = urllib2.Request(query)
            response = urllib2.urlopen(request)
            read = response.read()
            dictionary = json.loads(read)
            
            #process for function and add slider
            value = process(slider["process"],dictionary)
            slider["value"] = value
        
        objects["sliders"].append(slider)

    #3.2 build button objects
    objects["buttons"] = {}
    for button in inputs["buttons"]:
        continue   # not implemented yet....

    #4. return input objects to GUI
    return json.dumps(objects)

def process(function, dictionary):
    if function == 'count':
        return len(dictionary)
    else:
        raise ValueError,"Function not known: " + function
                              
def output(model_file, data):
    #6. run model with data
    cmd = 'python {0} work {1}'.format(model_file, ' '.join(data))
    output = os.popen(cmd).read().strip()

    #7. give data back to gui
    return output

known_models = {'Affordable':'StrawMan.py','311Calls':'StrawMan.py'}   # this can be a pickled list of known bobs
known_data_sets = {'311':'http://data.cityofnewyork.us/resource/erm2-nwe9.json?'}
if __name__ == '__main__':
    try:    
        model = sys.argv[1]  # the bob that the user wants to use
        action = sys.argv[2]
    except IndexError:
        sys.exit('IndexError: Not enough input provided')

    #check that model is familiar
    if model not in known_models:
        sys.exit(1,model,'is not a known model.')
    model_file = known_models[model]  
    
    if action == 'input':
        #1. GUI requests the use of a model
        print input_(model_file)
    elif action == 'output':
        #2. 
        print output(model_file, sys.argv[3:])
    else:
        print "Unknown:",action
