import uvicorn
from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
from typing import Literal, List, Union
import joblib
import json
import xgboost as xgb
from preprocess import preprocessing_data, preparation_data

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

@app.get("/")
async def message() :
    texte = "Estimation of rental price with xgboost machine learning model"
    return texte

@app.post("/predict", tags=["ML-Model-Prediction"])
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
    regressor = joblib.load("finalmodel.joblib")

    Y_pred = regressor.predict(X_val)
    print(Y_pred)
    response = {"Predicted rental price per day in dollars" : round(Y_pred.tolist()[0], 1)}
    
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)