# -*- coding: utf-8 -*-
"""
Created on Sun May 18 08:34:11 2014

@author: Lucio

Example GUI for use with Framework.py. When run at the command
line, the GUI displays the known models. If you click on a model
the GUI will use the framework to determine the GUI components
and their initial values. Clicking the 'run' button will call
the Framework to run the model with the values in the sliders.
Output from the model will be presented in a new Frame attached
to the GUI.

My (lucio) intention is that someone will build a web equivalent
of this. 

"""


from Tkinter import *
import tkMessageBox
import time
import Framework
import json

class gui (Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        master.title="SmarterCities"
        self.pack()
        
        self.file_for = {'Affordable':'StrawMan.py','311 Calls':'StrawMan.py'}  # this can be a pickled list of known models
        self.known_data_sets = {'311':'http://data.cityofnewyork.us/resource/erm2-nwe9.json?'}
        self.control_variables = {}
        self.buttons = {}

        self.create_widgets()
            
    def create_widgets(self):
        """Create the basic panel to display models"""
        #1. load models
        model_frame = Frame(root, bd = 5, bg='white', width=50, relief=GROOVE)
        model_frame.grid_propagate(0)
        
        Label(model_frame, text='Known models :', bg='white').pack(side=TOP)
        for model in self.file_for:
            b = Button(model_frame, text = model, height = 10, width = 10, 
                       bg='white', bd=5, 
                       command = lambda: self.make_panel_for(model))
            b.pack(side="left", padx=10, pady=10)
        model_frame.pack(side=TOP, fill=BOTH, padx=10, pady=10)
        
    def make_panel_for(self, model):
        """Create a panel for the parameter inputs for the *model*"""
        new_frame = Frame(root, bd=5, bg='white', relief=GROOVE)
        
        objects = Framework.input_(self.file_for[model])
        objects = json.loads(objects)
        Label(new_frame, text=model, bg='white').pack(side='left')
        self.control_variables[model] = []
        for slider in objects["sliders"]:
            v = DoubleVar()
            v.set(float(slider["value"]))
            self.control_variables[model].append(v)
            s = Scale(new_frame, from_=slider["min"], to=slider["max"], 
                      variable = v, orient=HORIZONTAL, bg='white', bd=0, 
                      label=slider["name"]+" :", length=200)
            s.pack(side="top", padx=5, pady=5)
        for button in objects["buttons"]:
            continue
        
        b = Button(new_frame, text="play", bg='white', 
               command=lambda: self.run_model(model))
        b.pack(side="top", pady=5)
        
        new_frame.pack(side=TOP, fill=BOTH, padx=10, pady=10)
            
    def run_model(self,model):
        """ Run *model* with parameters in the control variables"""
        parameters = [str(v.get()) for v in self.control_variables[model]]
        graphs = Framework.output(self.file_for[model], parameters)
        graphs = json.loads(graphs)
        try:
            import matplotlib.pyplot as plt
            for graph in graphs:
                plt.figure()
                plt.plot(map(float,graph['x']), map(float, graph['y']))
                plt.xlabel(graph['xlabel'])
                plt.ylabel(graph['ylabel'])
                plt.title(graph['title'])
        except ImportError:
            for graph in graphs:
                new_frame = Frame(root, bd=5, bg='white', relief=GROOVE)
                Label(new_frame, text=graph["title"], bg='white', justify=LEFT).pack(side=TOP, anchor='w')
                Label(new_frame, text="parameters:" + " ".join(parameters), bg='white', justify=LEFT).pack(side=TOP, anchor='w')
                Label(new_frame, text=str(graph["values"]), bg='white').pack(side=TOP)
                new_frame.pack(side=TOP, fill=BOTH, padx=10, pady=10)
                
root = Tk()
app = gui(master=root)
app.mainloop()
