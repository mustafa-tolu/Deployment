import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

import pickle

# --------------------------

html_temp = """
<div style="background-color:#8F0860; padding:1.5px">
<h1 style="color:white;text-align:center;">CAR PRICE PREDICTION </h1>
</div><br>"""
st.markdown(html_temp, unsafe_allow_html=True)

# --------------------------

col1, col2, col3 = st.columns([2,4,1]) # 2. col's width is larger

col1.write("")

img = Image.open("car-models.jpg")
col2.image(img, width=300)

col3.write("")

st.write("\n\n"*2)

# --------------------------

filename = 'Auto_Price_Pred_Model'
model = pickle.load(open(filename, 'rb'))

# --------------------------

st.sidebar.markdown('## :racing_car: Car Specs to Predict Price :racing_car:')
st.sidebar.write("\n\n")

form = st.form(key='my_form')

make_model = form.sidebar.selectbox("Model Selection", ("Audi A3", "Audi A1", "Opel Insignia", "Opel Astra", "Opel Corsa", "Renault Clio", "Renault Espace", "Renault Duster"))
hp_kW = form.sidebar.number_input("Horse Power:",min_value=40, max_value=294, value=120, step=5)
age = form.sidebar.number_input("Age:",min_value=0, max_value=3, value=0, step=1)
km = form.sidebar.number_input("km:",min_value=0, max_value=317000, value=10000, step=5000)
Gears = form.sidebar.number_input("Gears:",min_value=5, max_value=8, value=5, step=1)
Gearing_Type = form.sidebar.radio("Gearing Type", ("Manual", "Automatic", "Semi-automatic"))

submit_button = form.form_submit_button(label='Predict')

my_dict = {"make_model":make_model, "hp_kW":hp_kW, "age":age, "km":km, "Gears":Gears, "Gearing_Type":Gearing_Type}
df = pd.DataFrame.from_dict([my_dict])

cols = {
    "make_model": "Car Model",
    "hp_kW": "Horse Power",
    "age": "Age",
    "km": "km Traveled",
    "Gears": "Gears",
    "Gearing_Type": "Gearing Type"
}

df_show = df.copy()
df_show.rename(columns = cols, inplace = True)
st.write("Selected Specs: \n")
st.table(df_show)

# --------------------------

if submit_button:
    pred = model.predict(df)
    col4, col5, col6, col7 = st.columns([3,1,2,2])
    col4.write("The estimated value of car price is € ")
    col5.write(pred[0].astype(int))
    col6.write("")
    col7.write("")

    # --------------------------

#    col8, col9, col10 = st.columns([1,5,1])
#    with col8:
#        st.write("")
#    with col9:
#        img = Image.open("car-shadow.jpg")
#        st.image(img)
#    with col10:
#        st.write("")


st.write("\n\n")


