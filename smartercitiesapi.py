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
from flask import Flask, request, jsonify

app = Flask(__name__)

models = {"ExampleModel":"ExampleModel.py", "SmarterHousing":"SmarterHousing.py"}

@app.route("/")
def index():
    return jsonify({
        'title': 'SmarterCities',
        'readme': 'Visit https://smartercities.mybluemix.net/api for info on using the API'
        })

@app.route("/input/")
@app.route("/input/<model>", methods=['GET'])
def input_(model=None):
    #1. Try to get model
    if model is None:
        return jsonify({
            'error': 'model not provided -- use /input/model_name',
            })
    elif model not in models:
        return jsonify({
            'error': 'unknown model:{0}'.format(model),
            })
            
    #2. request data needs from bob
    model_file = models[model]
    cmd = 'python {0} request'.format("models/{0}".format(model_file))
    model_response = os.popen(cmd).read().strip()
    try:
        inputs = json.loads(model_response)
    except ValueError:
        return jsonify({
            'error': 'received non-JSON response from model',
            'response':model_response
        })
    
    #3. Build objects dictionary for data
    objects = {"model":model, "success":True}
    
    #3.1 build slider objects
    objects["sliders"] = []
    if "sliders" in inputs:
        for slider in inputs["sliders"]:
            #build api query
            if "data" in slider:
                #make query
                query = slider["data"]
                requested = urllib2.Request(query)
                response = urllib2.urlopen(requested)
                read = response.read()
                dictionary = json.loads(read)
                
                #process for function and add slider
                value = process(slider["process"],dictionary)
                slider["value"] = value
            
            objects["sliders"].append(slider)
        

    #3.2 build button objects
    objects["buttons"] = {}
    if "buttons" in inputs:
        for button in inputs["buttons"]:
            continue   # not implemented yet....
        
    #3.3 build rectangle objections
    if "rectangles" in inputs:
        objects["rectangle"] = inputs["rectangles"]

    #4. return input objects to GUI
    return jsonify(objects)

def process(function, dictionary):
    if function == 'count':
        return len(dictionary)
    else:
        raise ValueError,"Function not known: " + function
                 
@app.route("/output/")
@app.route("/output/<model>", methods=['GET'])
def output(model=None):
    if model is None:
        return jsonify({
            'error': 'model not provided -- use /input/model_name',
            })
    elif model not in models:
        return jsonify({
            'error': 'unknown model:{0}'.format(model),
            })
#    else:
#        try:
#            return jsonify({
#                'success':True,
#                'data':request.args
#                })
#        except ValueError:
#            return jsonify({
#                'error': 'request key didnt work',
#                'response': model
#            })
        
    
    #6. run model with data
    model_file = models[model]
    cmd = 'python {0} work {1}'.format("models/{0}".format(model_file), ' '.join(request.args.values()))
    output = os.popen(cmd).read().strip()
    
    #7. give data back to gui
    return jsonify({"cmd":cmd,"output":output})

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', port=int(port))

#known_data_sets = {'311':'http://data.cityofnewyork.us/resource/erm2-nwe9.json?'}
#if __name__ == '__main__':
#    try:    
#        model_file = sys.argv[1]  # the bob that the user wants to use
#        action = sys.argv[2]
#    except IndexError:
#        sys.exit('IndexError: Not enough input provided')
#    
#    if action == 'input':
#        #1. GUI requests the use of a model
#        print input_(model_file)
#    elif action == 'output':
#        #2. 
#        print output(model_file, sys.argv[3:])
#    else:
#        print "Unknown Action:",action
