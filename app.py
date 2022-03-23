from matplotlib import image
import streamlit as st
import pickle
import sklearn
import pandas as pd 
import numpy as np 
from PIL import Image
from pipeline import run_df_dc , run_df_lille, run_df_dc_personalised


df_app = ''

# On instancie le model 
savedmodel = open('./lgbm.pkl', 'rb')
model = pickle.load(savedmodel)
savedmodel.close()

# App configs
st.set_page_config(
page_title="Bike Sharing Demand Prediction",
layout="centered",
initial_sidebar_state="expanded",
)

ville = st.sidebar.radio(
     "Quelle ville souhaitez-vous ?",
     ('Lille', 'Washington DC'))


genre = st.sidebar.radio(
     "Quelle type de prédiction souhaitez-vous ?",
     ('Automatique', 'Manuel'))


if ville == 'Washington DC' :
    
    # Heading
    image = Image.open('CapitalBikeshare_Logo.jpg')
    st.image(image, width=150)

    # About 
    st.write("Capital Bikeshare is a bicycle-sharing system which serves Washington, D.C.; Arlington County, Virginia; the cities of Alexandria, Virginia and Falls Church, Virginia; Montgomery County, Maryland and Fairfax County, Virginia. As of May 2021, it had 627 stations and 5 400 bicycles.")
    st.write("Nearly 9 322 daily users who use our services in our 658 stations.")
    st.write("Learn more on our website : www.capitalbikeshare.com")
    
    
    if genre =='Automatique':
        
        # Creation of datafram 
        df_app = run_df_dc()
        array_1 = df_app.iloc[-1:,:]
        
        
    elif genre == 'Manuel':
        
        date = st.sidebar.date_input("Entrer la date :")
        time = st.sidebar.time_input("Entrer l'heure (HH24:MM):")
        day = st.sidebar.selectbox("Est on un jour férié ou un jour de vacance ?", ['Jour de vacance', 'Journée de travail', 'Weekend'])
        weather = st.sidebar.selectbox("Quelle est la météo ?", 
                    ['Ciel dégagé/légérement nuageux', 
                    'Brume/Nuageux', 
                    'Légère pluie/Légére chute de neige/Nuages eparpillé',
                        'Forte Pluie/Chute de neige/Brouilard/Orage'])
        temp = st.sidebar.text_input("Quelle est la température (en °C) ?")
        humidity = st.sidebar.text_input("Quel est le pourcentage d'humidité ?")
        windspeed = st.sidebar.text_input("Quel est la vitesse du vent ? (in km/h):")
        
        df_app = run_df_dc_personalised(date=date, time=time, day=day, weather=weather, temp=temp, temp_feel=temp, humidity=humidity, windspeed=windspeed)
        array_1 = df_app.iloc[-1:,:]


    
elif ville =='Lille':
    
        # Heading
        image = Image.open('logo_vlille.png')
        st.image(image, width=150)
        
        # About 
        st.write("Inauguré le 16 septembre 2011, V'Lille est le système de vélos en libre-service la métropole lilloise.")
        st.write("Dès son lancement, le service compte 2 000 abonnés dont 1 700 pour le libre-service. L'objectif affiché était d'arriver à 20 000 abonnés, libre-service et location longue durée confondus, d'ici 2015.")
        st.write("Après deux mois de fonctionnement, V'Lille compte 80 000 abonnés aux vélos en libre-service et 600 000 locations enregistrées.")
        st.write("Au 1er janvier 2020, il compte 2200 vélos répartis sur 223 stations, ce qui en fait un des éléments phares du système vélo de la métropole lilloise, qui compte environ 1000 km² de pistes et voies cyclables.")
        st.write("Rejoignez-nous sur : https://www.ilevia.fr/cms/institutionnel/velo/vlille/ ")
        
        if genre == 'Automatique' :
            
            # Creation of datafram 
            df_app = run_df_lille()
            array_1 = df_app.iloc[-1:,:]
        
        elif genre == 'Manuel':
        
            date = st.sidebar.date_input("Entrer la date :")
            time = st.sidebar.time_input("Entrer l'heure (HH24:MM):")
            day = st.sidebar.selectbox("Est on un jour férié ou un jour de vacance ?", ['Jour de vacance', 'Journée de travail', 'Weekend'])
            weather = st.sidebar.selectbox("Quelle est la météo ?", 
                        ['Ciel dégagé/légérement nuageux', 
                        'Brume/Nuageux', 
                        'Légère pluie/Légére chute de neige/Nuages eparpillé',
                        'Forte Pluie/Chute de neige/Brouilard/Orage'])
            temp = st.sidebar.text_input("Quelle est la température (en °C) ?")
            humidity = st.sidebar.text_input("Quel est le pourcentage d'humidité ?")
            windspeed = st.sidebar.text_input("Quel est la vitesse du vent ? (in km/h):")
            
            df_app = run_df_dc_personalised(date=date, time=time, day=day, weather=weather, temp=temp, temp_feel=temp, humidity=humidity, windspeed=windspeed)
            array_1 = df_app.iloc[-1:,:]


if st.button("Prédiction") :
    
    prediction = int(model.predict(array_1))   
    st.write("*A approximativement " + str(int(array_1['hour'].values)) + "h , heure locale, et en ce jour de week-end, et étant donnée l'ensoleillement, l'humidité et la vitesse du vent, il faudra  approximativement " + str(prediction) + " vélos loués sur cette station*. :sunglasses: ")

markdown =  '------------------------------------ \n Made by students of Simplon - Microsoft Dev IA formation'
st.markdown(markdown)
