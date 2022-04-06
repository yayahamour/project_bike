from os import stat
import numpy as np
import pandas as pd 
from contextlib import closing
from urllib.request import urlopen
import json
from datetime import datetime 

from tools.selectfield import * 


# J'importe et je modifie le df de train pour en faire le df de prédiction de base avec les colonnes dans le bonnes ordres. 
def make_df_init(index):
    df = pd.read_csv('./data/train.csv')
    df.drop('Unnamed: 0', axis=1, inplace = True)
    df.drop('datetime', axis=1, inplace=True)
    df.drop(columns=['registered', 'casual'], index=1, inplace=True)
    df = pd.DataFrame(columns=df.drop('count', axis=1).keys(), index=np.arange(0,index,1))
   
    return df 

def stat_api_3h(df, lat, lon):
    date = []
    temp = []
    atemp = []
    humidity = []
    windspeed = []
    weather = []
    with closing(urlopen(f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=6bda77c15824913b0353424425dfeb64')) as f:
        cityEph = json.loads(f.read())
        for i in range(0, len(cityEph['list'])):
            temp.append(cityEph['list'][i]['main']['temp'])
            atemp.append(cityEph['list'][i]['main']['feels_like'])
            humidity.append(cityEph['list'][i]['main']['humidity'])
            windspeed.append(cityEph['list'][i]['wind']['speed'])
            weather.append(cityEph['list'][i]['weather'][0]['main'])
            date.append(cityEph['list'][i]['dt_txt'])
            
    df['day'] = [ i for i in date]
    df['hour']  = pd.to_datetime(df['day']).dt.hour
    df['year']  = pd.to_datetime(df['day']).dt.year
    df['day']  = pd.to_datetime(df['day']).dt.dayofyear
    df['temp'] = [ i for i in temp]
    df['atemp'] = [ i for i in atemp]
    df['humidity'] = [ i for i in humidity]
    df['windspeed'] = [ i for i in windspeed]
    df['weather'] = [ str(i) for i in weather]
    df['temp'] = df['temp'] - 273.15
    df['atemp'] = df['atemp'] - 273.15
    
    
def stat_api_1h(df, lat, lon):
    date = []
    temp = []
    atemp = []
    humidity = []
    windspeed = []
    weather = []
    with closing(urlopen(f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely&appid=6bda77c15824913b0353424425dfeb64')) as f:
        cityEph = json.loads(f.read())    
        for i in range(0, len(cityEph['hourly'])): 

            temp.append(cityEph['hourly'][i]['temp'])
            atemp.append(cityEph['hourly'][i]['feels_like'])
            humidity.append(cityEph['hourly'][i]['humidity'])
            windspeed.append(cityEph['hourly'][i]['wind_speed'])
            weather.append(cityEph['hourly'][i]['weather'][0]['main'])
            date.append(cityEph['hourly'][i]['dt'])
            
    
    df['temp'] = [ i for i in temp]
    df['atemp'] = [ i for i in atemp]
    df['humidity'] = [ i for i in humidity]
    df['windspeed'] = [ i for i in windspeed]
    df['weather'] = [ str(i) for i in weather]
    df['temp'] = df['temp'] - 273.15
    df['atemp'] = df['atemp'] - 273.15
    
    
    
    
def make_season_holiday_dc(df):

    # Season 
    df['season'][(df['day'] >= 78 ) & (df['day'] < 141 )] = 1
    df['season'][(df['day'] >= 141) & (df['day'] < 365 ) ] = 2
    df['season'][(df['day'] >= 365) & (df['day'] < 356 ) ] = 3
    df['season'][(df['day'] >= 356) | (df['day'] < 78 ) ] = 4

    # Holliday For Washington 
    df['holiday'] = 0 
    df['holiday'][(df['day'] >= 357) | (df['day'] <= 2 ) ] = 1
    df['holiday'][(df['day'] >= 52) & (df['day'] <= 56 ) ] = 1
    df['holiday'][(df['day'] >= 69) & (df['day'] <= 70 ) ] = 1
    df['holiday'][(df['day'] >= 101) & (df['day'] <= 108 ) ] = 1
    df['holiday'][(df['day'] >= 185) & (df['day'] <= 240 ) ] = 1
    df['holiday'][(df['day'] >= 279) & (df['day'] <= 283 ) ] = 1
    df['holiday'][(df['day'] >= 315) & (df['day'] <= 329 ) ] = 1

    # Férié for Washington 
    df['holiday'][df['day'] == 17 ] = 1
    df['holiday'][df['day'] == 26 ] = 1
    df['holiday'][df['day'] == 150 ] = 1
    df['holiday'][df['day'] == 129 ] = 1
    df['holiday'][df['day'] == 305 ] = 1
    df['holiday'][df['day'] == 308 ] = 1
        
    df['workingday'] = 0
    for i in np.arange(1,365,7):
        df['workingday'][(df['day'] == i) | (df['day'] == i + 1) ] = 1
        
            
    df.rename(columns = {'weather' : 'weather2'}, inplace = True)
    df.insert(4, 'weather', 0)
    
    df['weather'][df['weather2'].str.lower().isin([weather_choice_1_from_api, weather_choice_1_from_page.lower()])] = 1
    df['weather'][df['weather2'].str.lower().isin([weather_choice_2_from_api, weather_choice_2_from_page.lower()])] = 2
    df['weather'][df['weather2'].str.lower().isin([weather_choice_3_from_api, weather_choice_3_from_page.lower()])] = 3
    df['weather'][df['weather2'].str.lower().isin([weather_choice_4_from_api, weather_choice_4_from_page.lower()])] = 4
    df.drop('weather2', axis=1, inplace=True)
    
    df['weather'] = df['weather'].astype(int)
    df['season'] = df['season'].astype(int)

    
    
def make_season_holiday_fr(df):

    # just need columns day to run this functions and 

    # Season 
    df['season'][(df['day'] >= 78 ) & (df['day'] < 141 )] = 1
    df['season'][(df['day'] >= 141) & (df['day'] < 365 ) ] = 2
    df['season'][(df['day'] >= 365) & (df['day'] < 356 ) ] = 3
    df['season'][(df['day'] >= 356) | (df['day'] < 78 ) ] = 4


    # Holliday France - Lille
    df['holiday'] = 0 
    df['holiday'][(df['day'] >= 352) | (df['day'] < 3 ) ] = 1
    df['holiday'][(df['day'] >= 36) & (df['day'] < 52 ) ] = 1
    df['holiday'][(df['day'] >= 99) & (df['day'] < 115 ) ] = 1
    df['holiday'][(df['day'] >= 145) & (df['day'] < 150 ) ] = 1
    df['holiday'][(df['day'] >= 188) & (df['day'] < 244 ) ] = 1
    df['holiday'][(df['day'] >= 296) & (df['day'] < 312 ) ] = 1

    # Férié 
    df['holiday'][df['day'] == 17 ] = 1
    df['holiday'][df['day'] == 26 ] = 1
    df['holiday'][df['day'] == 150 ] = 1
    df['holiday'][df['day'] == 129 ] = 1
    df['holiday'][df['day'] == 305 ] = 1
    df['holiday'][df['day'] == 308 ] = 1

    df['workingday'] = 0
    for i in np.arange(1,365,7):
        df['workingday'][(df['day'] == i) | (df['day'] == i + 1) ] = 1
        
        
    df.rename(columns = {'weather' : 'weather2'}, inplace = True)
    df.insert(4, 'weather', 0)
        
    df['weather'][df['weather2'].str.lower().isin([weather_choice_1_from_api, weather_choice_1_from_page.lower()])] = 1
    df['weather'][df['weather2'].str.lower().isin([weather_choice_2_from_api, weather_choice_2_from_page.lower()])] = 2
    df['weather'][df['weather2'].str.lower().isin([weather_choice_3_from_api, weather_choice_3_from_page.lower()])] = 3
    df['weather'][df['weather2'].str.lower().isin([weather_choice_4_from_api, weather_choice_4_from_page.lower()])] = 4
    df.drop('weather2', axis=1, inplace=True)
    
    df['weather'] = df['weather'].astype(int)
    df['season'] = df['season'].astype(int)
    
    
def add_day_hour_from_nom(df):

    day = datetime.now()
    df['day'] = day                          
    df['hour']  = pd.to_datetime(df['day']).dt.hour
    df['year']  = pd.to_datetime(df['day']).dt.year
    df['day']  = pd.to_datetime(df['day']).dt.dayofyear
    
    for i in range(0, len(df['hour'])):
        
        df.iloc[i,9] += i 
        if df.iloc[i,9] >= 24 :
            df.iloc[i,9] -= 24
            df.iloc[i,8] += 1
        else:
            df.iloc[i,9] += 1 
    
    return df

    
    
    # Decalage horaire : -5h 
def converstion_fr_dc(df):
    
        for i in range(0, len(df['hour'])):
        
            if df.iloc[i,9] <= 4 :
                df.iloc[i,9] += 19
            else:
                df.iloc[i,9] -= 5
        

    
    
# faire graph count vélo par jour des 20 jours précédents la requêtes + 10 des jours suivants 