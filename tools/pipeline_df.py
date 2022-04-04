import pandas as pd 
from tools.pipeline_function import *

# Data pour Lille à voir si utilisable  
# https://opendata.lillemetropole.fr/explore/dataset/vlille-realtime/table/

# Skip logs about pandas caveats documentations 
pd.options.mode.chained_assignment = None  # default='warn'



# Pipeline pour la prédiction personnalisée : 

def run_df_dc_personalised(df, date, time, weather, temp, temp_feel, humidity, windspeed):
    
    # Day of year 
    # print(time[0:2])
    
    df.iloc[0:1,3]= str(weather)
    df.iloc[0:1,4] = int(temp)
    df.iloc[0:1,5]= int(temp_feel)
    df.iloc[0:1,6] = int(humidity)
    df.iloc[0:1,7]= int(windspeed)
    df.iloc[0:1,8]=  pd.to_datetime(str(date)).dayofyear   
    time = str(time) 
    df.iloc[0:1,9] = int(time[0:2])
    
    make_season_holiday_dc(df)

    print(df.info())
    
    return df



# Pipeline pour la prediction automatique pour Washington DC : 
def run_df_dc():
        
    df_app = make_df_init(index=40)
    stat_api_3h(df_app, lat='38.8951', lon='77.0364')  
    make_season_holiday_dc(df_app)
    converstion_fr_dc(df_app)
    return df_app


# Pipeline pour la prediction automatique pour Lille : 

def run_df_lille():
    
    # Prendre la 1ere lignes du datafram pour le jour d'aujourd'hui
    df_app = make_df_init(index=40)
    stat_api_3h(df_app, lat='50.62925', lon='3.057256')
    make_season_holiday_fr(df_app)
    return df_app


def run_df_meteo_1h_lille():
    
    # Prendre la 1ere lignes du datafram pour le jour d'aujourd'hui
    df_app = make_df_init(48)
    stat_api_1h(df_app, lat='50.62925', lon='3.057256')
    add_day_hour_from_nom(df_app)
    make_season_holiday_fr(df_app)
    return df_app


def run_df_meteo_1h_dc():
    
    # Prendre la 1ere lignes du datafram pour le jour d'aujourd'hui
    df_app = make_df_init(48)
    stat_api_1h(df_app, lat='38.8951', lon='77.0364')   
    add_day_hour_from_nom(df_app)
    make_season_holiday_fr(df_app)
    converstion_fr_dc(df_app)
    return df_app


