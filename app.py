from matplotlib import image
import streamlit as st
import pickle
import sklearn
import pandas as pd 
import numpy as np 
from PIL import Image
from Pipeline.pipeline_df import run_df_dc , run_df_lille, run_df_dc_personalised




class Interface:
    
    def __init__(self):
        savedmodel = open('./lgbm.pkl', 'rb')
        self.model = pickle.load(savedmodel)
        savedmodel.close()
        st.set_page_config(
        page_title="Bike Sharing Demand Prediction",
        layout="centered",
        initial_sidebar_state="expanded",
        )
        image = Image.open('logo_vlille.png')
        st.image(image)

        st.write("Inauguré le 16 septembre 2011, V'Lille est le système de vélos en libre-service la métropole lilloise.\nDès son lancement, le service compte 2 000 abonnés dont 1 700 pour le libre-service. L'objectif affiché était d'arriver à 20 000 abonnés, libre-service et location longue durée confondus, d'ici 2015.\nAprès deux mois de fonctionnement, V'Lille compte 80 000 abonnés aux vélos en libre-service et 600 000 locations enregistrées.\nAu 1er janvier 2020, il compte 2200 vélos répartis sur 223 stations, ce qui en fait un des éléments phares du système vélo de la métropole lilloise, qui compte environ 1000 km² de pistes et voies cyclables.\nRejoignez-nous sur : https://www.ilevia.fr/cms/institutionnel/velo/vlille/ ")
        markdown =  '------------------------------------ \n Made by students of Simplon - Microsoft Dev IA formation'
        st.markdown(markdown)


    def sidebar(self):
        self.date = st.sidebar.date_input("Entrer la date :")
        self.time = st.sidebar.time_input("Entrer l'heure (HH24:MM):")
        self.day = st.sidebar.selectbox("Est on un jour férié ou un jour de vacance ?", ['Jour de vacance', 'Journée de travail', 'Weekend'])
        self.weather = st.sidebar.selectbox("Quelle est la météo ?", 
            ['Ciel dégagé/légérement nuageux', 
            'Brume/Nuageux', 
            'Légère pluie/Légére chute de neige/Nuages eparpillé',
            'Forte Pluie/Chute de neige/Brouilard/Orage'])
        self.temp = st.sidebar.text_input("Quelle est la température (en °C) ?", value=0)
        self.humidity = st.sidebar.text_input("Quel est le pourcentage d'humidité ?", value=0)
        self.windspeed = st.sidebar.text_input("Quel est la vitesse du vent ? (in km/h):", value=0)
            
        self.df_app = run_df_dc_personalised(date=self.date, time=self.time, weather=self.weather, temp=self.temp, temp_feel=self.temp, humidity=self.humidity, windspeed=self.windspeed)
        self.array_1 = self.df_app.iloc[-1:,:]

    def buton(self):
        if st.sidebar.button("Prédiction") :
            tab = str(self.date).split('-')
            tab1 = str(self.time).split(':')
            prediction = int(self.model.predict(self.array_1))   
            st.success("L'estimation de location sur la plage horraire de "+ str(int(self.array_1['hour'].values)) + "h  est de " + str(prediction) + " vélos sur cette station.\n\nL'estimation à été effectué pour le " + tab[2]+'/'+tab[1]+'/'+tab[0] + " à " + tab1[0] + "h"+ tab[1]+ 'm' +", avec une météo de type " + str(self.weather) + " avec une température de " + str(int(self.array_1['temp'])) + "° un taux d'humidité de " + str(int(self.array_1['humidity'])) + " % et un vent de " + str(int(self.array_1['windspeed'])) + "km/h.")
       
        m = st.markdown("""
        <style>
        div.stButton > button:first-child {
        background-color: #ffffff;
        color:#000000;
        }=
        </style>""", unsafe_allow_html=True)

app = Interface()
app.sidebar()
app.buton()
