import streamlit as st
import pickle
import sklearn 
import pandas as pd 
import numpy as np 

# App configs
st.set_page_config(
page_title="Bike Sharing Demand Prediction",
layout="centered",
initial_sidebar_state="expanded",
)

# Heading
st.markdown("<h1 style='text-align: center; background-color:deepskyblue'>🚴 Bike Rental Demand Prediction 🚴</h1>", 
            unsafe_allow_html=True)
# Sub heading
st.markdown("<h4 style='text-align: center'><i>∞∞∞ A Machine Learning based web app to predict bike rental demand ∞∞∞</i></h4>",
            unsafe_allow_html=True)
# Image
st.markdown("<h1 align='center'><img src='https://storage.googleapis.com/kaggle-competitions/kaggle/3948/media/bikes.png'></img></h1>", 
            unsafe_allow_html=True)



# About 
st.write("Bike sharing systems are a means of renting bicycles where the process of obtaining membership, rental, and bike return is automated via a network of kiosk locations throughout a city. Using these systems, people are able rent a bike from a one location and return it to a different place on an as-needed basis.")
st.write("This project is based on a Kaggle competition. Our task is to combine historical usage patterns with weather data in order to forecast bike rental demand in the Capital Bikeshare program in Washington, D.C.")
st.markdown("<i>For more details on this competition, [visit here](https://www.kaggle.com/c/bike-sharing-demand).</i>", unsafe_allow_html=True)

st.markdown("<br><h4><b> Please fill in the below details:</b></h4><br>", unsafe_allow_html=True)

from pipeline import run_df
from lightgbm import LGBMRegressor 

# Creation of datafram 
df_app = run_df()
array = df_app.iloc[-1:,:]

# User input features
date = st.date_input("Enter date :")
time = st.time_input("Enter Time (HH24:MM):")
day = st.selectbox("What type of day is it?", ['Holiday', 'Working day', 'Weekend'])
weather = st.selectbox("What type of weather is it?", 
             ['Clear/Few clouds', 
              'Mist/Cloudy', 
              'Light Rain/Light Snow/Scattered clouds',
              'Heavy Rain/Snowfall/Foggy/Thunderstorm'])
temp = st.text_input("Enter temperature (in °C):")
humidity = st.text_input("Enter humidity (in %):")
windspeed = st.text_input("Enter windspeed (in km/h):")

if st.button("Predict Rentals"):

    if ((date=='') | (time=='') | (day=='') | (weather=='') | 
        (temp=='') | (humidity=='') | (windspeed=='')):
        st.error("Please fill all fields before proceeding.")
    else :
        # You will have to create the model
        df = pd.DataFrame()
        df['date'] = date
        df['date'] = pd.to_datetime(df['date']).dt.dayofyear
        #                    season	holiday	workingday	weather	temp	atemp	humidity	windspeed	day	   hour
        savedmodel = open('lgbm.pkl', 'rb')
        model = pickle.load(savedmodel)
        savedmodel.close()
        # array = np.array([[1, 0, 0, 1, int(temp), 18, 20, 0.2,  12, 2]])

        prediction = int(model.predict(array))   
        st.success("There will be an approx. demand of " + str(prediction) + " bikes for above conditions.")

