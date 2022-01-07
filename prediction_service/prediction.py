
from flask import Flask,render_template,request,jsonify 
import os
import yaml
import joblib
import numpy as np
import json



params_path = "params.yaml"
schema_path = os.path.join("prediction_service", "schema_in.json") #min and max values for our parmaters are stored in schema

class NotInRange(Exception):
    def __init__(self, message="Values entered are not in expected range"):
        self.message = message
        super().__init__(self.message)

class NotInCols(Exception):
    def __init__(self, message="Not in cols"):
        self.message = message
        super().__init__(self.message)


def read_params(config_path=params_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def predict(data):

    config = read_params(params_path)  
    model_dir_path = config["webapp_model_dir"] #gets the machine learning model
    model = joblib.load(model_dir_path)  #loads the model 
    prediction = model.predict(data).tolist()[0]  #[0] , does not return list

    #target column shld be btw 3-8 range

    try:
        if 3 <= prediction <= 8:
            return prediction
        else:
            raise NotInRange
    except NotInRange:
        return "Unexpected result"
        

#gets the schema ie min and max values for our features
def get_schema(schema_path=schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema

def validate_input(dict_request): 
    
    def _validate_cols(col):
        schema = get_schema()  #gets schema  structure and values

        actual_cols = schema.keys() #ie the name of keys (of dict)
        if col not in actual_cols:   #if appropriate columns are not present then
            raise NotInCols 


    def _validate_values(col, val):
        schema = get_schema()
       #the values shld be between min and max
        if not (schema[col]["min"] <= float(dict_request[col]) <= schema[col]["max"]) : 
            raise NotInRange
    
    for col, val in dict_request.items(): #iteratinh over dict 
        _validate_cols(col)  #validating the name of columns (for each column we have a min and max value)
        _validate_values(col, val) #validating the range of values ie checking fro min and max
    return True

def form_response(dict_request):
    if validate_input(dict_request):
        data = dict_request.values() #we are getting only values and not keys 
        data = [list(map(float, data))]  #converting str to float using map and converting to list (as it creates map object)
        response = predict(data)
        return response

def api_response(dict_request):   
    try:
        if validate_input(dict_request):

            data = np.array([list(dict_request.values())])
            response = predict(data)
            response = {"response":response} #return as json

            return response
    except Exception as e :
   #if an error is thrown then the user is given with appropriate min and max values for params
   #ie. with  get_schema() file
        response = {"the expected range is :":get_schema(), "response": str(e)}
        return response