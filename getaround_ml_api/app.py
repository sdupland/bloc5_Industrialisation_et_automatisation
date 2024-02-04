#import libraries we need
import uvicorn # provide an asynchrone interface between python web app and web servers, necessary with fastapi
from fastapi import FastAPI # help building API in an easy way and good performance
import pandas as pd
from pydantic import BaseModel # basemodel is a class used to define data models
from typing import Literal, List, Union # typing provides a set of classes for working with types and type hints abd specify expected types of variables for example
from joblib import load
import xgboost as xgb
from preprocess import preprocessing_data, preparation_data # personnal functions found in preprocess.py script

# description
description = """
Estimation of rental price based on different features, with xgboost machine learning model.
the input is a dictionary with the following items :
model_key: str
mileage: Union[int, float]
engine_power: Union[int, float]
fuel: str
paint_color: str
car_type: str
private_parking_available: bool
has_gps: bool
has_air_conditioning: bool
automatic_car: bool
has_getaround_connect: bool
has_speed_regulator: bool
winter_tires: bool
"""

# tags to identify different endpoints
tags_metadata = [{"name": "ML-Model-Prediction","description": "Estimation of rental price with xgboost machine learning model"}]

app = FastAPI(
    title="Getaround API",
    description=description,
    version="0.1",
    contact={
        "name": "sndd",
        "url": "https://github.com/sdupland",
    },
    openapi_tags=tags_metadata)

# define for each feature the type of data (integer, boulean, float), the default value, and if necessary a list of possible values
class Features(BaseModel):
    model_key: Literal["Citroën","Renault","BMW","Peugeot","Audi","Nissan","Mitsubishi","Mercedes","Volkswagen","Toyota","others","SEAT","Subaru","PGO","Opel","Ferrari"] = "Citroën"
    mileage: Union[int, float]
    engine_power: int
    fuel: Literal["diesel","petrol","others"]="diesel"
    paint_color: Literal["black","grey","blue","white","brown","silver","red","beige","others"]="black"
    car_type: Literal["convertible","coupe","estate","sedan","suv","subcompact","hatchback","van"]="estate"
    private_parking_available: bool=True
    has_gps: bool=True
    has_air_conditioning: bool=False
    automatic_car: bool=False
    has_getaround_connect: bool=False
    has_speed_regulator: bool=False
    winter_tires: bool=True

# decorator in FastAPI that associates the function message() with the specified route between coma ("/") and the HTTP GET method
@app.get("/")
# The message() function is defined as an asynchronous function
# This allows asynchronous operations to be performed within the function.
# When someone accesses the root URL ("/") of the application using a web browser or any HTTP client, they will receive the text "Estimation of rental price with xgboost machine learning model" as the response.
async def message() :
    texte = "Estimation of rental price with xgboost machine learning model"
    return texte


# uses the @app.post decorator to associate the function predict() with the HTTP POST method at the "/predict" endpoint
@app.post("/predict", tags=["ML-Model-Prediction"])
# the predict function is defined as an asynchronous function
# It takes a parameter Features
# it expects a request body containing data with a structure defined by the Features model.
async def predict(Features: Features):
    """
    Calculate the price per day for a specific rental car
    
    params : inputs needs a dictionary of values for the followin items :
    model_key: str
    mileage: Union[int, float]
    engine_power: Union[int, float]
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool

    return : the function returns a float number which is the predicted price of a car with
    the characteristics given in input
    
    """
    df1 = preparation_data(Features)
    
    X_val = preprocessing_data(df1)

    # Load the model
    regressor = load("finalmodel.joblib")

    Y_pred = regressor.predict(X_val)
    print(Y_pred)
    response = {"Predicted rental price per day in dollars" : round(Y_pred.tolist()[0], 1)}
    
    return response

if __name__ == "__main__": # checks if the script is being executed as the main program
    #  If the script is being run as the main program (i.e., not imported as a module), this line is executed. It uses the uvicorn.run() function to run a FastAPI application (app) using the Uvicorn ASGI server.
    uvicorn.run(app, host="0.0.0.0", port=4000)