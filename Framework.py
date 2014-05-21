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

def build_interface_for(bob_file):
    #request data needs from bob
    bob_response = os.popen('python {0} request'.format(bob_file)).read().strip()
    bob_needs = json.loads(bob_response)
    
    #grab data needs from some source
    objects = {"sliders":[], "buttons":[]}
    for data_set in bob_needs:
        query = known_data_sets[data_set["data_name"]]

        for slider in data_set["sliders"]:
            #go through key/values and build api query
            for i in range(len(slider["keys"])):
                query+=slider["keys"][i]+'='+slider["values"][i]+'&'
    
            #make query
            request = urllib2.Request(query)
            response = urllib2.urlopen(request)
            read = response.read()
            dictionary = json.loads(read)
            
            #process for function and add slider
            value = process(slider["function"],dictionary)
            slider["value"] = value
            
            objects["sliders"].append(slider)

        objects["buttons"] = {}
        for button in data_set["buttons"]:
            continue   # not implemented yet....

        #return data to GUI
        return json.dumps(objects)
                              
def run(bob_file, data):
        #run bob with data
        cmd = 'python {0} work {1}'.format(bob_file, ' '.join(data))
        output = os.popen(cmd).read().strip()

        #give data back to gui
        return output


def process(function, dictionary):
    if function == 'count':
        return len(dictionary)
    else:
        raise ValueError,"Function not known: " + function

known_bobs = {'lucio':'lucio.py'}  # this can be a pickled list of known bobs
known_data_sets = {'311':'http://data.cityofnewyork.us/resource/erm2-nwe9.json?'}
if __name__ == '__main__':
    try:    
        bob = sys.argv[1]  # the bob that the user wants to use
        action = sys.argv[2]
    except IndexError:
        sys.exit('IndexError: Not enough input provided')

    #load known bobs and possible data sets
    if bob not in known_bobs:  # i.e. not a known 'bob'
        sys.exit(1,bob,'not a known BOB.')
    bob_file = known_bobs[bob]  
    
    if action == 'input':
        print build_interface_for(bob_file)
    elif action == 'output':
        print run(bob_file, sys.argv[3:])
    else:
        print "action not known:",action
