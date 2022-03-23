from matplotlib import image
import streamlit as st
import pickle
import sklearn 
import pandas as pd 
import numpy as np 
from PIL import Image
from pipeline import run_df_dc , run_df_lille


df_app = ''

# On instancie le model 
savedmodel = open('lgbm.pkl', 'rb')
model = pickle.load(savedmodel)
savedmodel.close()

# App configs
st.set_page_config(
page_title="Bike Sharing Demand Prediction",
layout="centered",
initial_sidebar_state="expanded",
)

genre = st.sidebar.radio(
     "Quelle ville souhaitez-vous ?",
     ('Lille', 'Washington DC'))

if genre == 'Washington DC':
    # Creation of datafram 
    df_app = run_df_dc()
    array_1 = df_app.iloc[-1:,:]
else:
    df_app = run_df_lille()
    array_1 = df_app.iloc[-1:,:]


genre = st.sidebar.radio(
     "Quelle type de prédiction souhaitez-vous ?",
     ('Automatique', 'Manuel'))

if genre == 'Automatique':
    st.write(" ")
else:
     # User input features
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



# Heading
image = Image.open('logo_vlille.png')
st.image(image)

# About 
st.write("Inauguré le 16 septembre 2011, V'Lille est le système de vélos en libre-service la métropole lilloise.")
st.write("Dès son lancement, le service compte 2 000 abonnés dont 1 700 pour le libre-service. L'objectif affiché était d'arriver à 20 000 abonnés, libre-service et location longue durée confondus, d'ici 2015.")
st.write("Après deux mois de fonctionnement, V'Lille compte 80 000 abonnés aux vélos en libre-service et 600 000 locations enregistrées.")
st.write("Au 1er janvier 2020, il compte 2200 vélos répartis sur 223 stations, ce qui en fait un des éléments phares du système vélo de la métropole lilloise, qui compte environ 1000 km² de pistes et voies cyclables.")


if st.button("Prédiction"):
    # You will have to create the model
    #                    season	holiday	workingday	weather	temp	atemp	humidity	windspeed	day	   hour

    prediction = int(model.predict(array_1))   
    st.success("A approximativement " + str(int(array_1['hour'].values)) + "h , et en ce jour de week-end, et étant donnée l'ensoleillement, l'humidité et la vitesse du vent, il faudra  approximativement " + str(prediction) + " vélos loués sur cette station.")

markdown =  '------------------------------------ \n                                                Made by students of Simplon - Microsoft Dev IA formation'
st.markdown(markdown)