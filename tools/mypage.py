from dataclasses import dataclass 
import numpy as np 
from PIL import Image
import streamlit as st
from tools.pipeline_df import run_df_dc , run_df_lille, run_df_dc_personalised, run_df_meteo_1h_lille, run_df_meteo_1h_dc
from tools.selectfield import * 
import pickle
from PIL import Image
import seaborn as sns 
import matplotlib.pyplot as plt 
from datetime import datetime
import json
import requests
from tools.api_azure import api_azure


# Definition of my dataclass Page 
@dataclass
class Page:
    
    ville : str = ""
    df_app = run_df_lille()
    genre : str = 'Automatique'
    graph : str = ""
    date : str = ""
    time : int = 0
    weather : str = ""
    temp : int = 0
    temp_feel : int = 0
    humidity : int = 0
    windspeed : int = 0
    model_selector : str = "" 
    model : str = ""
    choices : str = ""

    # Run pages
    def  run_page(self):
        
        if self.ville == 'Lille':
            if self.prediction_config == 'Aucun':

                # Heading
                image = Image.open('./image/logo_vlille.png')
                st.image(image,  width=500)
                st.write('--------------------------------------------------------') 
                # About 
                st.write(vlille_presentation)
                st.write(vlille_info_1)
                st.write(vlille_info_2)
                st.write(vlille_info_3)
                st.write(vlille_contact_info)
                # Apply the good predict datafram
                st.write('--------------------------------------------------------')

            
            if self.choices == 'Views 5 days':     
                self.df_app = run_df_lille()
                # Voir pour intégrer le df_app = pd.read_sql() ou pd.read_sql_query('select * from df_lille_1h', con) ? 
            else:
                self.df_app = run_df_meteo_1h_lille()
            if self.genre == 'Personnalisée':
                self.df_app = run_df_dc_personalised( df=self.df_app, date=self.date, time=self.time, weather=self.weather, temp=self.temp, temp_feel=self.temp, humidity=self.humidity, windspeed=self.windspeed)
                
        elif self.ville == "Washington DC":
            if self.prediction_config == 'Aucun':

                # Heading
                image = Image.open('./image/CapitalBikeshare_Logo.jpg')
                st.image(image, width=500)
                st.write('--------------------------------------------------------')
                # About 
                st.write(washington_info_1)
                st.write(washington_info_2)
                st.write(washington_info_3)
                # Apply the good predict datafram
                st.write('--------------------------------------------------------')
            
            if self.choices == 'Views 5 days':
                self.df_app = run_df_dc()
            else:
                self.df_app = run_df_meteo_1h_dc()
            if self.genre =='Personnalisée':
                self.df_app = run_df_dc_personalised( df=self.df_app, date=self.date, time=self.time, weather=self.weather, temp=self.temp, temp_feel=self.temp, humidity=self.humidity, windspeed=self.windspeed)

        
            
    def  sidebar(self):
        
        self.model_selector = st.sidebar.selectbox("Selection du modèle de prediction", ['xgboost', 'lgbm',"stacking"])       
        self.ville = st.sidebar.radio("Quelle ville souhaitez-vous prédir ?", ['Lille', 'Washington DC'])      
        self.prediction_config = st.sidebar.radio("Options :", ['Aucun','Predictions','Alertes'])     

        
        if self.prediction_config == 'Predictions':

            self.choices = st.sidebar.selectbox("Select duration:" , ['Views 5 days', 'Views 24 hours'])
            
            self.genre = st.sidebar.radio("Quelle type de prédiction souhaitez-vous ?", ['Instantannée', 'Personnalisée'])
            
            if self.genre == 'Personnalisée' :
                self.date = st.sidebar.date_input("Enter the date :")
                self.time = st.sidebar.time_input("Enter hour :")
                self.weather = st.sidebar.selectbox("What is the weather ?", 
                            ['Clear/Few clouds', 
                            'Mist/Cloudy', 
                            'Light Rain/Light Snow/Scattered clouds',
                                'Heavy Rain/Snowfall/Foggy/Thunderstorm'])
                self.humidity = st.sidebar.slider("Enter humidity (in %) ?", 0, 100)
                self.temp = st.sidebar.slider("Enter temperature (in °C) ?", -30 , 55, value=0)
                self.windspeed = st.sidebar.slider("Enter windspeed ? (in km/h):", 0, 150)  

            
        elif self.prediction_config == 'Alertes':
            self.alert = st.sidebar.selectbox("Programmer une alerte ?", ['Desactive', 'Activé'])                    
            if self.alert == 'Activé':
                level_max = st.sidebar.slider("A partir de combien de vélo attendu ?", 0, 550)
                self.alert = st.sidebar.selectbox("Programmer une alerte ?", ['Par email', 'Par sms'])
                st.sidebar.button('Programmer une alerte')
        
    
    def convert(self, df):
        dic = {}
        for i, row in df.iterrows():
            dic[str(i)] = row.to_dict()
        return({"data" : dic})

    def prediction(self):
        if (self.model_selector != "azure"): # Modele Azure deleted for now
            r = requests.post(url='https://api-bike-braz.herokuapp.com/predict/'+self.model_selector, data=(json.dumps(self.convert(self.df_app))))    
            # Prediction en fonction de la premiere ligne du datafram
            pred = eval(r.json())
        else :
            pred = eval(api_azure(self.df_app))["Results"]
            print(type(pred))
            
        self.df_app = self.df_app.fillna(self.df_app.mean())
        self.df_app['pred'] = pred
        prediction_row = self.df_app.iloc[0:1,:]
        # display the dataffram for debugging  
        # st.write(self.df_app)            
        
        page_date = str(self.date).split('-')
        page_time = str(self.time).split(':')   
        date_now = datetime.now()
        dt_now = str(date_now).split(' ')
        dt_date = [ i for i in dt_now[0]] # date 
        dt_hour = [ i for i in dt_now[1]] # heure 
        st.title('Rental bike viewer:')
        st.write('Resultat of instant prediction:')

        
        # Affichage de la réponse de prédictions :
        st.success("A environ "+ str(int(prediction_row['hour'])) + "h, heure de " +  self.ville  + ", l'IA entraînnnée par un modéle " + self.model_selector + " s'attend à une demande de **" + str(int(prediction_row['pred'])) + " vélos.**")
        
        if self.genre == "Personnalisée":
            st.write("Informations about prediction :")
            st.success("\n\n**L'estimation à été effectuée pour le " + page_date[2]+'/'+page_date[1]+'/'+page_date[0] + " soit, étant le " + str(int(prediction_row['day'])) + "ème jour de l'année, à " + page_time[0] + "h"+ page_time[1]+ 'm' +", pour une météo de type " + str(self.weather) + " avec une température de " + str(int(prediction_row['temp'])) + "°, un taux d'humidité de " + str(int(prediction_row['humidity'])) + "% et un vent de " + str(int(prediction_row['windspeed'])) + "km/h pour " + self.ville + ".**")
        else:
            st.write("Informations about prediction :")
            st.success("\n\n**L'estimation à été effectuée pour ce " + dt_date[8] + dt_date[9] + "/" + dt_date[5] + dt_date[6] +  "/"   + dt_date[0] + dt_date[1] + dt_date[2] + dt_date[3] + " soit, étant le " + str(int(prediction_row['day'])) + "ème jour de l'année, à " +  str(int(prediction_row['hour'])) + "h"+ dt_hour[3] + dt_hour[4] +"m, considérant la météo et pour une température de " + str(int(prediction_row['temp'])) + "°, un taux d'humidité de " + str(int(prediction_row['humidity'])) + " % et un vent de " + str(int(prediction_row['windspeed'])) + "km/h pour " + self.ville + ".**")
       
        st.write('--------------------------------------------------------')
       
       
       
    def graphiques (self):
        
        col1, col2 = st.columns(2)
        fig, ax = plt.subplots()
        
        index = int(self.df_app.loc[0,['hour']])
        
        with col1 :
            sns.barplot(data = self.df_app.iloc[0:6,:], x=np.arange(index,index + 6,1), y='pred')
            plt.title('Predictions pour les 6 prochaines heures')
            st.pyplot(fig) 
        with col2:
            plt.title('Predictions des demandes en vélos par journée')
            sns.barplot(data = self.df_app, x='day', y='pred')
            st.pyplot(fig)  
            
        if self.prediction_config == 'Predictions':
            if self.choices == 'Views 5 days':
                df_pred = self.df_app.copy()
                df_pred.index = df_pred['hour']


                # st.area_chart(self.df_app)
                st.write('--------------------------------------------------------')
                st.write('Prediction des demandes en vélo pour les 15 prochaines heures')
                st.bar_chart(df_pred.loc[:,['pred']])
                st.write('--------------------------------------------------------')
                
                
            elif self.choices == 'Views 24 hours':
                df_app = self.df_app.copy()
                # st.area_chart(self.df_app)
                st.write('--------------------------------------------------------')
                st.write('Prediction des demandes en vélo pour les 15 prochaines heures')
                st.bar_chart(self.df_app.loc[:15,['pred']])
                st.write('--------------------------------------------------------')
                
                
    def init_page(self):
        
        # App configs
        st.set_page_config(
        page_title="Bike Sharing Demand Prediction",
        layout="centered",
        initial_sidebar_state="expanded",
        )
        self.sidebar()
        self.run_page()
        self.prediction()
        self.graphiques()



            
        