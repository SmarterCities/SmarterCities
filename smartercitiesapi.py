"""

API for SmarterCities application. 

"""

import sys
import os
import json
import urllib2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

models = {"ExampleModel":"ExampleModel.py", "SmarterHousing":"SmarterHousing.py", "311Messages":"311Messages.py"}

@app.route("/")
#@cross_origin()
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
            'known models': models.keys()
            })
    elif model not in models:
        return jsonify({
            'error': 'unknown model:{0}'.format(model),
            'known models': models.keys()
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
    objects["buttons"] = inputs["buttons"]

    #3.3 build rectangle objections
    objects["entries"] = inputs["entries"]

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
            'success': False,
            'error': 'model not provided -- use /output/model_name',
            'known models': models.keys()
            })
    elif model not in models:
        return jsonify({
            'success': False,
            'error': 'unknown model:{0}'.format(model),
            'known models': models.keys()
            })
    
    #6. run model with data
    model_file = models[model]
    args = ""
    for key in request.args:
        args+=key + " " + request.args[key] + " "
    cmd = 'python {0} work {1}'.format("models/{0}".format(model_file), args)
    try:
        output = os.popen(cmd).read().strip()
        objects = {'output':json.loads(output)}
    
        #7. give data back to gui
        objects['cmd'] = cmd
        objects['success'] = True
        return jsonify(objects)
    except Exception as e:
        return jsonify({'success':False, 
                        'requests':request.args,
                        'cmd':cmd,
                        'exception': str(e),
                        'output':output})

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', port=int(port))
