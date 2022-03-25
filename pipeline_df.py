from os import stat
import numpy as np
import pandas as pd 
import datetime as dt 
from contextlib import closing
from urllib.request import urlopen
import json
from pipeline_function import *

# Data pour Lille à voir si utilisable  
# https://opendata.lillemetropole.fr/explore/dataset/vlille-realtime/table/


# Pipeline pour la prediction automatique pour Washington DC : 
def run_df_dc():
        
    df_app = make_df_init()
    stat_api_3h(df_app, lat='38.8951', lon='77.0364')    
    make_season_holiday_dc(df_app)
    return df_app



# Pipeline pour la prediction automatique pour Lille : 

def run_df_lille():
    
    # Prendre la 1ere lignes du datafram pour le jour d'aujourd'hui
    df_app = make_df_init()
    stat_api_3h(df_app, lat='50.62925', lon='3.057256')
    make_season_holiday_fr(df_app)
    return df_app



# Pipeline pour la prédiction personnalisée : 

def run_df_dc_personalised(date, time, weather, temp, temp_feel, humidity, windspeed):

    df_app = make_df_init()

    # Day of year 
    df_app['day']  = date
    df_app['day']  = pd.to_datetime(df_app['day']).dt.dayofyear
    time = str(time) 
    df_app['hour'] = int(time[-8:-6])

    df_app['temp'] = int(temp)
    df_app['atemp'] = int(temp_feel)
    df_app['humidity'] = int(humidity)
    df_app['windspeed'] = int(windspeed)
    df_app['weather'] = str(weather)

    make_season_holiday_fr(df_app)
    
    
    return df_app