import numpy as np
import pandas as pd 
import datetime as dt 
from contextlib import closing
from urllib.request import urlopen
import json



# https://opendata.lillemetropole.fr/explore/dataset/vlille-realtime/table/

# Enelever jour de vacance car on le calcule automatiquement avec la date ? 
# Refaire Holiday et les jours ferié pour la piepline de france 

# faire graph count vélo par jour des 20 jours précédents la requêtes + 10 des jours suivants 

# Phrase impliquant tout les facteurs de la prédictions. 


# Dans la date de ma requete api je dois récuperer le mois et l'année pour le transformer en dayofyear. 




# ---------------------------------------------------------------- Pipeline pour la prediction automatique pour Washington DC : 

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


    # Holliday Washington DC
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
        df_app['workingday'][(df_app['day'] == i) | (df_app['day'] == i + 1) ] = 1
        
        
        
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




# ---------------------------------------------------------------- Pipeline pour la prediction automatique pour Lille : 

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


    # Holliday France - Lille
    df_app['holiday'] = 0 
    df_app['holiday'][(df_app['day'] >= 352) & (df_app['day'] < 3 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 36) & (df_app['day'] < 52 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 99) & (df_app['day'] < 115 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 145) & (df_app['day'] < 150 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 188) & (df_app['day'] < 244 ) ] = 1
    df_app['holiday'][(df_app['day'] >= 296) & (df_app['day'] < 312 ) ] = 1

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
        df_app['workingday'][(df_app['day'] == i) | (df_app['day'] == i + 1) ] = 1
        
        
        
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




# ---------------------------------------------------------------- Pipeline pour la prédiction personnalisée : 

def run_df_dc_personalised(date, time, day, weather, temp, temp_feel, humidity, windspeed):
    df = pd.read_csv('./data/train.csv')
    df.drop('Unnamed: 0', axis=1, inplace = True)
    df.drop('datetime', axis=1, inplace=True)
    df.drop(columns=['registered', 'casual'], index=1, inplace=True)
    df_app = pd.DataFrame(columns=df.keys(), index=np.arange(1,5,1))

    # Day of year 
    df_app['day']  = date
    df_app['day']  = pd.to_datetime(df_app['day']).dt.dayofyear
    time = str(time) 
    df_app['hour'] = int(time[-8:-6])


    # Season 
    df_app['season'][df_app['day'] < 172 ] = 1
    df_app['season'][(df_app['day'] >= 172) & (df_app['day'] < 264 ) ] = 2
    df_app['season'][(df_app['day'] >= 264) & (df_app['day'] < 356 ) ] = 3
    df_app['season'][(df_app['day'] >= 356) | (df_app['day'] < 172 ) ] = 4


    # Holliday Washington DC
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


    df_app['temp'] = int(temp)
    df_app['atemp'] = int(temp_feel)
    df_app['humidity'] = int(humidity)
    df_app['windspeed'] = int(windspeed)
    df_app['weather'] = str(weather)
        
        
    # A refa
    df_app['workingday'] = 0
    for i in np.arange(1,365,7):
        df_app['workingday'][(df_app['day'] == i) | (df_app['day'] == i + 1) ] = 1
        
        
        
    df_app.rename(columns = {'weather' : 'weather2'}, inplace = True)
    df_app.insert(4, 'weather', "")


    # df_app['weather'][df_app['weather'].str.lower().isin(['clear', 'few clouds', 'partly cloudy'])] = 1
    df_app['weather'][df_app['weather2'].str.lower() == 'ciel dégagé/légérement nuageux'] = 1
    df_app['weather'][df_app['weather2'].str.lower() == 'brume/nuageux'] = 2
    df_app['weather'][df_app['weather2'].str.lower() == 'légère pluie/légére chute de neige/nuages eparpillé'] = 3
    df_app['weather'][df_app['weather2'].str.lower() == 'forte pluie/chute de neige/brouilard/orage'] = 4

    df_app['weather'] = df_app['weather'].astype(int)
    df_app['season'] = df_app['season'].astype(int)
    
    df_app.drop('weather2', axis=1, inplace=True)
    df_app.drop('count', axis=1, inplace=True)
    

    
    return df_app



# ---------------------------------------------------------------- Fonction qui créer un datafram avec 40 lignes à predir avec les API météo pour Lille pour 5j et par 3h
# ---------------- Refaire la partie heure et jour pour récupérer au bon format et utiliser convert datetime comme j'ai fait pour convertir dateofyear a voir pour simplifier -----------------------


def run_df_meteo_lille():
    df = pd.read_csv('./data/train.csv')
    df.drop('Unnamed: 0', axis=1, inplace = True)
    df.drop('datetime', axis=1, inplace=True)
    df.drop(columns=['registered', 'casual'], index=1, inplace=True)
    df_meteo_lille = pd.DataFrame(columns=df.drop('count', axis=1).keys(), index=np.arange(0,40,1))


    date = [] 
    jour_meteo = []
    heure_meteo = []
    with closing(urlopen('http://api.openweathermap.org/data/2.5/forecast?lat=50.62925&lon=3.057256&appid=6bda77c15824913b0353424425dfeb64')) as f:
        cityEph = json.loads(f.read())
        for i in range(0, len(cityEph['list'])):
            # print(cityEph['list'][i]['main']['temp'])
            df_meteo_lille['temp'] = cityEph['list'][i]['main']['temp']
            df_meteo_lille['atemp'] = cityEph['list'][i]['main']['feels_like']
            df_meteo_lille['humidity'] = cityEph['list'][i]['main']['humidity']
            df_meteo_lille['windspeed'] = cityEph['list'][i]['wind']['speed']
            df_meteo_lille['weather'] = cityEph['list'][i]['weather'][0]['main']
            
            
            date += cityEph['list'][i]['dt_txt']
            j1_start = 0
            j1_stop = 10
            h1_start = 11 
            h1_stop = 13
            day_after = 19     

            jour = [date[j1_start + (day_after *i):j1_stop + (day_after *i)]]
            hour = [date[h1_start + (day_after *i):h1_stop + (day_after *i)]]
            jour_meteo.append(''.join([str(item) for item in jour]))
            heure_meteo.append(hour)
        
        liste_heure = []
        for i in heure_meteo:
            a = i[0][0]
            b = i[0][1]
            num = int(a + b)
            liste_heure.append(num)
                
        df_meteo_lille['hour'] = liste_heure

        liste_jour = []
        for i in jour_meteo:
            for j in i :
                try:
                    liste_jour.append(int(j))
                        
                    
                except :
                    pass
        liste_jour

        liste_final = []

        for j in liste_jour:
            # print(j)
            # print(type(j))
            if j  not in [']','[',',', ' ']:
                liste_final.append(j)

        liste_final

        liste_final_2 = []
        a = ""
        for i in range(0, len(liste_final), 8):
            num = liste_final[i : i+8 ]
            num_transformed = str(num)
            # print(num_transformed)
            for j in num_transformed:
                if j  not in [']','[',',', ' ']:
                    # print(j)
                    # print(type(j))
                    a += str(j)
            
        liste_final_2
        a

        num = ""
        for i in range(0, len(a), 8):
            num += a[i : i+8 ]
            num += '-'
            

        df_meteo_lille['day'] = num[0:-1].split('-')
        df_meteo_lille['day']  = pd.to_datetime(df_meteo_lille['day']).dt.dayofyear


        # Season 
        df_meteo_lille['season'][df_meteo_lille['day'] < 172 ] = 1
        df_meteo_lille['season'][(df_meteo_lille['day'] >= 172) & (df_meteo_lille['day'] < 264 ) ] = 2
        df_meteo_lille['season'][(df_meteo_lille['day'] >= 264) & (df_meteo_lille['day'] < 356 ) ] = 3
        df_meteo_lille['season'][(df_meteo_lille['day'] >= 356) | (df_meteo_lille['day'] < 172 ) ] = 4


        # Holliday France - Lille
        df_meteo_lille['holiday'] = 0 
        df_meteo_lille['holiday'][(df_meteo_lille['day'] >= 352) & (df_meteo_lille['day'] < 3 ) ] = 1
        df_meteo_lille['holiday'][(df_meteo_lille['day'] >= 36) & (df_meteo_lille['day'] < 52 ) ] = 1
        df_meteo_lille['holiday'][(df_meteo_lille['day'] >= 99) & (df_meteo_lille['day'] < 115 ) ] = 1
        df_meteo_lille['holiday'][(df_meteo_lille['day'] >= 145) & (df_meteo_lille['day'] < 150 ) ] = 1
        df_meteo_lille['holiday'][(df_meteo_lille['day'] >= 188) & (df_meteo_lille['day'] < 244 ) ] = 1
        df_meteo_lille['holiday'][(df_meteo_lille['day'] >= 296) & (df_meteo_lille['day'] < 312 ) ] = 1

        # Férié 
        df_meteo_lille['holiday'][df_meteo_lille['day'] == 17 ] = 1
        df_meteo_lille['holiday'][df_meteo_lille['day'] == 26 ] = 1
        df_meteo_lille['holiday'][df_meteo_lille['day'] == 150 ] = 1
        df_meteo_lille['holiday'][df_meteo_lille['day'] == 129 ] = 1
        df_meteo_lille['holiday'][df_meteo_lille['day'] == 305 ] = 1
        df_meteo_lille['holiday'][df_meteo_lille['day'] == 308 ] = 1

        df_meteo_lille['workingday'] = 0
        for i in np.arange(1,365,7):
            df_meteo_lille['workingday'][(df_meteo_lille['day'] == i) | (df_meteo_lille['day'] == i + 1) ] = 1
            
        df_meteo_lille['temp'] = df_meteo_lille['temp'] - 273.15
        df_meteo_lille['atemp'] = df_meteo_lille['atemp'] - 273.15

        df_meteo_lille['weather'][df_meteo_lille['weather'].str.lower() == 'clear'] = 1
        df_meteo_lille['weather'][df_meteo_lille['weather'].str.lower().isin(['clouds','drizzle'])] = 2
        df_meteo_lille['weather'][df_meteo_lille['weather'].str.lower().isin(['snow','rain'])] = 3
        df_meteo_lille['weather'][df_meteo_lille['weather'].str.lower().isin(['heavy','extreme'])] = 4

        df_meteo_lille['weather'] = df_meteo_lille['weather'].astype(int)
        df_meteo_lille['season'] = df_meteo_lille['season'].astype(int)
        df_meteo_lille
                
    return df_meteo_lille




# ---------------------------------------------------------------- Fonction qui créer un datafram avec 40 lignes à predir avec les API météo pour Washignton pour 5j par 3h
# ---------------------------------------------------------------- Refaire la partie heure et jour pour récupérer au bon format et utiliser convert datetime 


def run_df_meteo_dc():
    df = pd.read_csv('./data/train.csv')
    df.drop('Unnamed: 0', axis=1, inplace = True)
    df.drop('datetime', axis=1, inplace=True)
    df.drop(columns=['registered', 'casual'], index=1, inplace=True)
    df_meteo_dc = pd.DataFrame(columns=df.drop('count', axis=1).keys(), index=np.arange(0,40,1))


    date = [] 
    jour_meteo = []
    heure_meteo = []
    with closing(urlopen('http://api.openweathermap.org/data/2.5/forecast?lat=38.8951&lon=-77.0364&appid=6bda77c15824913b0353424425dfeb64')) as f:
        cityEph = json.loads(f.read())
        for i in range(0, len(cityEph['list'])):
            # print(cityEph['list'][i]['main']['temp'])
            df_meteo_dc['temp'] = cityEph['list'][i]['main']['temp']
            df_meteo_dc['atemp'] = cityEph['list'][i]['main']['feels_like']
            df_meteo_dc['humidity'] = cityEph['list'][i]['main']['humidity']
            df_meteo_dc['windspeed'] = cityEph['list'][i]['wind']['speed']
            df_meteo_dc['weather'] = cityEph['list'][i]['weather'][0]['main']
            
            
            date += cityEph['list'][i]['dt_txt']
            j1_start = 8
            j1_stop = 10
            h1_start = 11 
            h1_stop = 13
            day_after = 19     
            jour = [date[j1_start + (day_after *i):j1_stop + (day_after *i)]]
            hour = [date[h1_start + (day_after *i):h1_stop + (day_after *i)]]
            jour_meteo.append(jour)
            heure_meteo.append(hour)
            
            
    a = ""
    b = ""
    num = ""
    liste_jour = []
    for i in jour_meteo:
        a = i[0][0]
        b = i[0][1]
        num = int(a + b)
        liste_jour.append(num)
        
    liste_heure = []
    for i in heure_meteo:
        a = i[0][0]
        b = i[0][1]
        num = int(a + b)
        liste_heure.append(num)
        

    df_meteo_dc['day'] = liste_jour
    df_meteo_dc['hour'] = liste_heure
    # Season 
    df_meteo_dc['season'][df_meteo_dc['day'] < 172 ] = 1
    df_meteo_dc['season'][(df_meteo_dc['day'] >= 172) & (df_meteo_dc['day'] < 264 ) ] = 2
    df_meteo_dc['season'][(df_meteo_dc['day'] >= 264) & (df_meteo_dc['day'] < 356 ) ] = 3
    df_meteo_dc['season'][(df_meteo_dc['day'] >= 356) | (df_meteo_dc['day'] < 172 ) ] = 4


    # Holliday Washington DC
    df_meteo_dc['holiday'] = 0 
    df_meteo_dc['holiday'][(df_meteo_dc['day'] >= 357) & (df_meteo_dc['day'] <= 2 ) ] = 1
    df_meteo_dc['holiday'][(df_meteo_dc['day'] >= 52) & (df_meteo_dc['day'] <= 56 ) ] = 1
    df_meteo_dc['holiday'][(df_meteo_dc['day'] >= 69) & (df_meteo_dc['day'] <= 70 ) ] = 1
    df_meteo_dc['holiday'][(df_meteo_dc['day'] >= 101) & (df_meteo_dc['day'] <= 108 ) ] = 1
    df_meteo_dc['holiday'][(df_meteo_dc['day'] >= 185) & (df_meteo_dc['day'] <= 240 ) ] = 1
    df_meteo_dc['holiday'][(df_meteo_dc['day'] >= 279) & (df_meteo_dc['day'] <= 283 ) ] = 1
    df_meteo_dc['holiday'][(df_meteo_dc['day'] >= 315) & (df_meteo_dc['day'] <= 329 ) ] = 1

    # Férié 
    df_meteo_dc['holiday'][df_meteo_dc['day'] == 17 ] = 1
    df_meteo_dc['holiday'][df_meteo_dc['day'] == 26 ] = 1
    df_meteo_dc['holiday'][df_meteo_dc['day'] == 150 ] = 1
    df_meteo_dc['holiday'][df_meteo_dc['day'] == 129 ] = 1
    df_meteo_dc['holiday'][df_meteo_dc['day'] == 305 ] = 1
    df_meteo_dc['holiday'][df_meteo_dc['day'] == 308 ] = 1

    df_meteo_dc['workingday'] = 0
    for i in np.arange(1,365,7):
        df_meteo_dc['workingday'][(df_meteo_dc['day'] == i) | (df_meteo_dc['day'] == i + 1) ] = 1
        
    df_meteo_dc['temp'] = df_meteo_dc['temp'] - 273.15
    df_meteo_dc['atemp'] = df_meteo_dc['atemp'] - 273.15
    
    df_meteo_dc['weather'][df_meteo_dc['weather'].str.lower() == 'clear'] = 1
    df_meteo_dc['weather'][df_meteo_dc['weather'].str.lower().isin(['clouds','drizzle'])] = 2
    df_meteo_dc['weather'][df_meteo_dc['weather'].str.lower().isin(['snow','rain'])] = 3
    df_meteo_dc['weather'][df_meteo_dc['weather'].str.lower().isin(['heavy','extreme'])] = 4
    
    df_meteo_dc['weather'] = df_meteo_dc['weather'].astype(int)
    df_meteo_dc['season'] = df_meteo_dc['season'].astype(int)
        
    return df_meteo_dc

