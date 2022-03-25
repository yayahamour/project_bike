from os import stat
import numpy as np
import pandas as pd 
import datetime as dt 
from contextlib import closing
from urllib.request import urlopen
import json



# J'importe et je modifie le df de train pour en faire le df de prédiction de base avec les colonnes dans le bonnes ordres. 
def make_df_init(paris=True):
    
    df = pd.read_csv('./data/train.csv')
    df.drop('Unnamed: 0', axis=1, inplace = True)
    df.drop('datetime', axis=1, inplace=True)
    df.drop(columns=['registered', 'casual'], index=1, inplace=True)
    df = pd.DataFrame(columns=df.drop('count', axis=1).keys(), index=np.arange(0,40,1))

    # Day of year 
    df['day'] = pd.to_datetime('today').normalize().dayofyear
    df['hour'] = pd.datetime.today()
    if paris:
        df['hour'] = df['hour'].dt.tz_localize('Etc/GMT-1').dt.tz_convert('Europe/Paris').dt.hour
    else:
        df['hour'] = df['hour'].dt.tz_localize('Etc/GMT-5').dt.tz_convert('Universal').dt.hour
    
    return df 

def stat_api_3h(df, lat, lon, days=False):
    date = []
    num = ""
    jour_meteo = []
    heure_meteo = []
    temp = []
    atemp = []
    humidity = []
    windspeed = []
    weather = []
    with closing(urlopen(f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=6bda77c15824913b0353424425dfeb64')) as f:
        cityEph = json.loads(f.read())
        
        
        for i in range(0, len(cityEph['list'])):
            # print(cityEph['list'][i]['main']['temp'])
            temp.append(cityEph['list'][i]['main']['temp'])
            atemp.append(cityEph['list'][i]['main']['feels_like'])
            humidity.append(cityEph['list'][i]['main']['humidity'])
            windspeed.append(cityEph['list'][i]['wind']['speed'])
            weather.append(cityEph['list'][i]['weather'][0]['main'])
            date.append(cityEph['list'][i]['dt_txt'])
            
    df['day'] = [ i for i in date]
    df['day']  = pd.to_datetime(df['day']).dt.dayofyear
    df['temp'] = [ i for i in temp]
    df['atemp'] = [ i for i in atemp]
    df['humidity'] = [ i for i in humidity]
    df['windspeed'] = [ i for i in windspeed]
    df['weather'] = [ str(i) for i in weather]
    
    
    
def make_season_holiday_dc(df):

    # Season 
    df['season'][(df['day'] >= 78 ) & (df['day'] < 141 )] = 1
    df['season'][(df['day'] >= 141) & (df['day'] < 365 ) ] = 2
    df['season'][(df['day'] >= 365) & (df['day'] < 356 ) ] = 3
    df['season'][(df['day'] >= 356) & (df['day'] < 78 ) ] = 4

    # Holliday For Washington 
    df['holiday'] = 0 
    df['holiday'][(df['day'] >= 357) & (df['day'] <= 2 ) ] = 1
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
    df.insert(4, 'weather', "")
    
    df['weather'][df['weather2'].str.lower().isin(['clear'])] = 1
    df['weather'][df['weather2'].str.lower().isin(['clouds','drizzle','mist'])] = 2
    df['weather'][df['weather2'].str.lower().isin(['snow','rain'])] = 3
    df['weather'][df['weather2'].str.lower().isin(['heavy','extreme'])] = 4
    
    df.drop('weather2', axis=1, inplace=True)

    df['weather'] = df['weather'].astype(int)
    df['season'] = df['season'].astype(int)
    
    
def make_season_holiday_fr(df):

    # just need columns day to run this functions and 

    # Season 
    df['season'][(df['day'] >= 78 ) & (df['day'] < 141 )] = 1
    df['season'][(df['day'] >= 141) & (df['day'] < 365 ) ] = 2
    df['season'][(df['day'] >= 365) & (df['day'] < 356 ) ] = 3
    df['season'][(df['day'] >= 356) & (df['day'] < 78 ) ] = 4


    # Holliday France - Lille
    df['holiday'] = 0 
    df['holiday'][(df['day'] >= 352) & (df['day'] < 3 ) ] = 1
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
        
    df['weather'][df['weather2'].str.lower().isin(['clear'])] = 1
    df['weather'][df['weather2'].str.lower().isin(['clouds','drizzle','mist'])] = 2
    df['weather'][df['weather2'].str.lower().isin(['snow','rain'])] = 3
    df['weather'][df['weather2'].str.lower().isin(['heavy','extreme'])] = 4
    df.drop('weather2', axis=1, inplace=True)
    
    df['weather'] = df['weather'].astype(int)
    df['season'] = df['season'].astype(int)
    
    

    
    
# faire graph count vélo par jour des 20 jours précédents la requêtes + 10 des jours suivants 