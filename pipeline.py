import numpy as np
import pandas as pd 
import datetime as dt 



# https://opendata.lillemetropole.fr/explore/dataset/vlille-realtime/table/

# faire graph count vélo par jour des 20 jours précédents la requêtes + 10 des jours suivants 

# Phrase impliquant tout les facteurs de la prédictions. 

def run_df_dc():
    df = pd.read_csv('./data/train.csv')
    df.drop('Unnamed: 0', axis=1, inplace = True)
    df.drop('datetime', axis=1, inplace=True)
    df.drop(columns=['registered', 'casual'], index=1, inplace=True)
    df_app = pd.DataFrame(columns=df.keys(), index=np.arange(1,5,1))
    
    # Day of year 
    df_app['day'] = pd.to_datetime('today').normalize().dayofyear
    df_app['hour'] = pd.datetime.today()
    df_app['hour'] = df_app['hour'].dt.tz_localize('Etc/GMT-5').dt.tz_convert('Universal').dt.hour


    # Season 
    df_app['season'][df_app['day'] < 172 ] = 1
    df_app['season'][(df_app['day'] >= 172) & (df_app['day'] < 264 ) ] = 2
    df_app['season'][(df_app['day'] >= 264) & (df_app['day'] < 356 ) ] = 3
    df_app['season'][(df_app['day'] >= 356) | (df_app['day'] < 172 ) ] = 4


    # Holliday 
    df_app['holiday'] = 0 
    df_app['holiday'][(df_app['day'] >= 357) & (df_app['day'] <= 2 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 52) & (df_app['day'] <= 56 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 69) & (df_app['day'] <= 70 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 101) & (df_app['day'] <= 108 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 185) & (df_app['day'] <= 240 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 279) & (df_app['day'] <= 283 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 315) & (df_app['day'] <= 329 ) ] = 1

    # Férié 
    df_app['holiday'][df_app['day'] == 17 ] = 1
    df_app['holiday'][df_app['day'] == 26 ] = 1
    df_app['holiday'][df_app['day'] == 150 ] = 1
    df_app['holiday'][df_app['day'] == 129 ] = 1
    df_app['holiday'][df_app['day'] == 305 ] = 1
    df_app['holiday'][df_app['day'] == 308 ] = 1


    from contextlib import closing
    from urllib.request import urlopen
    import json

    with closing(urlopen('https://api.openweathermap.org/data/2.5/weather?lat=38.9071923&lon=-77.0368707&appid=105c1c6fdcbbdebbb96de7d29b2fc7ff')) as f:
        cityEph = json.loads(f.read())
        # print(cityEph)
        # print(cityEph['wind']['speed'])
        df_app['temp'] = cityEph['main']['temp']
        df_app['atemp'] = cityEph['main']['feels_like']
        df_app['humidity'] = cityEph['main']['humidity']
        df_app['windspeed'] = cityEph['wind']['speed']
        df_app['weather'] = cityEph['weather'][0]['main']
        
        
    df_app['workingday'] = 0
    for i in np.arange(1,365,7):
        df_app['workingday'][(df_app['day'] == i) | (df_app['day'] == i) + 1 ] = 1
        
        
        
    df_app.rename(columns = {'weather' : 'weather2'}, inplace = True)
    df_app.insert(4, 'weather', "")


    # df_app['weather'][df_app['weather'].str.lower().isin(['clear', 'few clouds', 'partly cloudy'])] = 1
    df_app['weather'][df_app['weather2'].str.lower() == 'clear'] = 1
    df_app['weather'][df_app['weather2'].str.lower().isin(['clouds','drizzle'])] = 2
    df_app['weather'][df_app['weather2'].str.lower().isin(['snow','rain'])] = 3
    df_app['weather'][df_app['weather2'].str.lower().isin(['heavy','extreme'])] = 4
    df_app['weather'] = df_app['weather'].astype(int)
    df_app['season'] = df_app['weather'].astype(int)
    
    
    df_app['temp'] = df_app['temp'] - 273.15
    df_app['atemp'] = df_app['atemp'] - 273.15

    
    df_app.drop('weather2', axis=1, inplace=True)
    df_app.drop('count', axis=1, inplace=True)
    
    return df_app


def run_df_lille():
    df = pd.read_csv('./data/train.csv')
    df.drop('Unnamed: 0', axis=1, inplace = True)
    df.drop('datetime', axis=1, inplace=True)
    df.drop(columns=['registered', 'casual'], index=1, inplace=True)
    df_app = pd.DataFrame(columns=df.keys(), index=np.arange(1,5,1))

    # Day of year 
    df_app['day'] = pd.to_datetime('today').normalize().dayofyear
    df_app['hour'] = pd.datetime.today()
    df_app['hour'] = df_app['hour'].dt.tz_localize('Etc/GMT-1').dt.tz_convert('Europe/Paris').dt.hour


    # Season 
    df_app['season'][df_app['day'] < 172 ] = 1
    df_app['season'][(df_app['day'] >= 172) & (df_app['day'] < 264 ) ] = 2
    df_app['season'][(df_app['day'] >= 264) & (df_app['day'] < 356 ) ] = 3
    df_app['season'][(df_app['day'] >= 356) | (df_app['day'] < 172 ) ] = 4


    # Holliday 
    df_app['holiday'] = 0 
    df_app['holiday'][(df_app['day'] >= 357) & (df_app['day'] <= 2 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 52) & (df_app['day'] <= 56 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 69) & (df_app['day'] <= 70 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 101) & (df_app['day'] <= 108 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 185) & (df_app['day'] <= 240 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 279) & (df_app['day'] <= 283 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 315) & (df_app['day'] <= 329 ) ] = 1

    # Férié 
    df_app['holiday'][df_app['day'] == 17 ] = 1
    df_app['holiday'][df_app['day'] == 26 ] = 1
    df_app['holiday'][df_app['day'] == 150 ] = 1
    df_app['holiday'][df_app['day'] == 129 ] = 1
    df_app['holiday'][df_app['day'] == 305 ] = 1
    df_app['holiday'][df_app['day'] == 308 ] = 1


    from contextlib import closing
    from urllib.request import urlopen
    import json

    with closing(urlopen('https://api.openweathermap.org/data/2.5/weather?lat=38.9071923&lon=-77.0368707&appid=105c1c6fdcbbdebbb96de7d29b2fc7ff')) as f:
        cityEph = json.loads(f.read())
        # print(cityEph)
        # print(cityEph['wind']['speed'])
        df_app['temp'] = cityEph['main']['temp']
        df_app['atemp'] = cityEph['main']['feels_like']
        df_app['humidity'] = cityEph['main']['humidity']
        df_app['windspeed'] = cityEph['wind']['speed']
        df_app['weather'] = cityEph['weather'][0]['main']
        
        
    df_app['workingday'] = 0
    for i in np.arange(1,365,7):
        df_app['workingday'][(df_app['day'] == i) | (df_app['day'] == i) + 1 ] = 1
        
        
        
    df_app.rename(columns = {'weather' : 'weather2'}, inplace = True)
    df_app.insert(4, 'weather', "")


    # df_app['weather'][df_app['weather'].str.lower().isin(['clear', 'few clouds', 'partly cloudy'])] = 1
    df_app['weather'][df_app['weather2'].str.lower() == 'clear'] = 1
    df_app['weather'][df_app['weather2'].str.lower().isin(['clouds','drizzle'])] = 2
    df_app['weather'][df_app['weather2'].str.lower().isin(['snow','rain'])] = 3
    df_app['weather'][df_app['weather2'].str.lower().isin(['heavy','extreme'])] = 4
    df_app['weather'] = df_app['weather'].astype(int)
    df_app['season'] = df_app['weather'].astype(int)
    
    
    df_app['temp'] = df_app['temp'] - 273.15
    df_app['atemp'] = df_app['atemp'] - 273.15

    
    df_app.drop('weather2', axis=1, inplace=True)
    df_app.drop('count', axis=1, inplace=True)
    
    return df_app