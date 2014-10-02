SmarterCities
=============

This is the code repository for SmarterCities, an application that aims to to simulation and modeling in the hands of citizens of New York City and other metropolitan areas. Full documentation (will eventually be) available on our website at http://smartercities.mybluemix.net/api.

Basic Uses
-------------

The API entry point is 

	smartercities-api.mybluemix.net/

You can interact with a sample model by using the *input* tag and providing a model. Here's an example:

	smartercities-api.mybluemix.net/input/ExampleModel

The API returns the necessary input for ExampleModel, e.g. sliders, buttons, and rectangles. To run the model use the *output* tag and provide the values for each of the sliders:

	smartercities-api.mybluemix.net/output/ExampleModel?a=1&b=2&c=3&d=4&e=5
