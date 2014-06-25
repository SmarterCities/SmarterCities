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
import os

class gui (Frame):

    def __init__(self, master):
        self.width = 500
        Frame.__init__(self, master, width=self.width)
        master.title="SmarterCities"
        self.pack()
        
        models = os.popen('ls models').read().strip().split('\n')
        self.file_for = {m.replace('.py',''):'models/'+m for m in models}
        self.control_variables = {}
        self.buttons = {}

        self.create_widgets()
        self.new_frame = None  #  for deleteing old models
            
    def create_widgets(self):
        """Create the basic panel to display models"""
        #1. load models
        model_frame = Frame(root, bd = 5, bg='white', width=self.width, relief=GROOVE)
        model_frame.grid_propagate(0)
        
        Label(model_frame, text='Models :', bg='white').pack(side=TOP, anchor='w')
        v = StringVar()  
        for model in self.file_for.keys()[-1::-1]: #go backwards because the command = lambda is broken...
            b = Radiobutton(model_frame, text = model, value = model,
                            height = 10, width = 20, bg='white', bd=5,
                            variable = v, command = lambda: self.make_panel_for(v.get()))
            b.pack(side="left", padx=10, pady=10)
        model_frame.pack(side=TOP, fill=BOTH, padx=10, pady=10)
        
    def make_panel_for(self, model):
        """Create a panel for the parameter inputs for the *model*"""
        #clear old frame if necessary
        if self.new_frame:
            self.new_frame.destroy()
        
        #create new frame to hold model parameters
        self.new_frame = Frame(root, bd=5, bg='white', relief=GROOVE, width=1000)
        input_frame = Frame(self.new_frame)
        Label(input_frame, text=model, bg='white').pack(side='top',anchor='w')
        
        #put a play button at the top
        b = Button(input_frame, text="run", bg='white', command=lambda: self.run_model(model))
        b.pack(side="top", pady=5, anchor='w')
        
        #grab parameter objects from model
        #objects = Framework.input_(self.file_for[model])
        cmd = 'python Framework.py {0} input'.format(self.file_for[model])      
        output = os.popen(cmd).read().strip()
        objects = json.loads(output)
        
        self.control_variables[model] = []
        for slider in objects["sliders"]:
            v = DoubleVar()
            v.set(float(slider["value"]))
            self.control_variables[model].append(v)
            s = Scale(input_frame, from_=slider["min"], to=slider["max"], 
                      variable = v, bg='white', bd=0, orient=VERTICAL, 
                      label=slider["name"]+" :")
            s.pack(side="left", padx=5, pady=5)
        for button in objects["buttons"]:
            continue
        
        input_frame.pack(side=TOP, fill=BOTH)
        self.new_frame.pack(side=TOP, fill=BOTH, padx=10, pady=10)
            
    def run_model(self,model):
        """ Run *model* with parameters in the control variables"""
        parameters = [str(v.get()) for v in self.control_variables[model]]
        #graphs = Framework.output(self.file_for[model], parameters)
        cmd = 'python Framework.py {0} output {1}'.format(self.file_for[model], ' '.join(parameters))      
        output = os.popen(cmd).read().strip()
        graphs = json.loads(output)
        try:
            import matplotlib.pyplot as plt
            for graph in graphs:
                plt.plot(map(float,graph['x']), map(float, graph['y']))
                plt.xlabel(graph['xlabel'])
                plt.ylabel(graph['ylabel'])
                plt.title(graph['title'])
        except ImportError:
            for graph in graphs:
                graph_frame = Frame(self.new_frame, bd=5, bg='white', relief=GROOVE)
                Label(graph_frame, text=graph["title"], bg='white', justify=LEFT).pack(side=TOP, anchor='w')
                Label(graph_frame, text="values:" + " ".join(parameters), bg='white', justify=LEFT).pack(side=TOP, anchor='w')
                Label(graph_frame, text=str(graph["y"]), bg='white').pack(side=TOP)
                graph_frame.pack(side='top', fill=BOTH, padx=10, pady=10)
                
root = Tk()
app = gui(master=root)
app.mainloop()
