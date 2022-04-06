from fastapi import FastAPI, File, HTTPException, UploadFile, Path 
import uvicorn 
from flask import Flask, render_template, jsonify
import pickle 
from models import Topred, Data
import numpy as np 
import json 
import pandas as pd 



def load_model(model):
    # Pickle load model 
    if model == 'xgboost':
        savedmodel = open('./model/xgboost.pkl', 'rb')
        model = pickle.load(savedmodel)
        savedmodel.close()
    elif model == "lgbm":
        savedmodel = open('./model/lgbm.pkl', 'rb')
        model = pickle.load(savedmodel)
        savedmodel.close()
    return model


    
# def predict(data, model):
#     # We keep the 2 classes with the highest confidence score
#     model = load_model(model)
#     results = model.predict(data)
#     response = [
#         {"Prediction": result} for result in results
#     ]
#     return response


api = FastAPI()

from pydantic import BaseModel 


# Predict the all datafram 
@api.post("/predict/xgboost/all")
def prediction_lgbm( dico : Data):

    model = load_model('xgboost')
    season = []
    holiday = []
    workingday = []
    weather = []
    temp = []
    atemp = []
    humidity = []
    windspeed = []
    day = []
    hour = []
    year = []

    # Initialize the data dictionnary that will be returned

    dico = dico.dict()['data']

    for i in range(0,len(dico)):
        data = dico[str(i)]

    
        season.append(data['season'])
        holiday.append(data['holiday'])
        workingday.append(data['workingday'])
        weather.append(data['weather'])
        temp.append(data['temp'])
        atemp.append(data['atemp'])
        humidity.append(data['humidity'])
        windspeed.append(data['windspeed'])
        day.append(data['day'])
        hour.append(data['hour'])
        year.append(data['year'])

    pred = {'season' : season, 'holiday' : holiday, 'workingday' : workingday, 'weather' : weather, 'temp' : temp, 'atemp' : atemp, 'humidity' : humidity, 'windspeed' :windspeed, 'day' :day, 'hour' : hour, 'year' : year }
    df = pd.DataFrame(pred, index=np.arange(0,len(dico)))

    print('print du df :', df)
    result = model.predict(df)
    # print('resultat fin de fonction', result)
    print('result:', result)
    response = []
    for i in result:
        response.append(int(i)) 
    
    return json.dumps(response)




# To predict one row of the datafram 
@api.post("/predict/xgboost/row")
def prediction_lgbm( data : Topred ):
    print('print data début de fonction: ', data)

    model = load_model('xgboost')

    # Initialize the data dictionnary that will be returned
    print('print du season :', data.dict())
    data = data.dict()

    season = data['season']
    holiday = data['holiday']
    workingday = data['workingday']
    weather = data['weather']
    temp = data['temp']
    atemp = data['atemp']
    humidity = data['humidity']
    windspeed = data['windspeed']
    day = data['day']
    hour = data['hour']
    year = data['year']

    pred = {'season' : season, 'holiday' : holiday, 'workingday' : workingday, 'weather' : weather, 'temp' : temp, 'atemp' : atemp, 'humidity' : humidity, 'windspeed' :windspeed, 'day' :day, 'hour' : hour, 'year' : year }
    df = pd.DataFrame(pred, index=[0])

    print('print du df :', df)
    result = model.predict(df)
    print('resultat fin de fonction', result)
    response = {'Result of prediction' : int(result)} 
    
    return json.dumps(response), 200


# One get for test
@api.get("/")
@api.get("/predict/")
def pred():

    # response = json.dumps({'a' : 'test'})
    
    return {'Bonjour' : "Bonjour"}


if __name__ == "__main__":
    uvicorn.run(api, host="127.0.0.1", port=8000, log_level="info")

