from matplotlib import image
import streamlit as st
import pickle
import sklearn
import pandas as pd 
import numpy as np 
from PIL import Image
from Pipeline.pipeline_df import run_df_dc , run_df_lille, run_df_dc_personalised
from myclass import Interface

def main():
    app = Interface()
    app.sidebar()
    app.buton()

main()