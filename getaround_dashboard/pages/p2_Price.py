import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Config
st.set_page_config(
    page_title="Getaround Data analysis",
    layout="wide"
)

# App
st.title("Price analysis")

@st.cache_data()
def load_data():
    path = "data/dataset_price_clean.csv"
    data = pd.read_csv(path)
    return data

dataset_price = load_data()

# Content
st.sidebar.header("Table of content")
st.sidebar.markdown("""
    * [Preview of data set](#dataset-preview)
    * [Graph 1](##plot-1) - Mean rental price per day
    * [Graph 2](#plot-2) - Evolution of mean price according to the options
    * [Graph 3](#plot-3) - Type of models rented according to the kind of fuel
    * [Graph 4](#plot-4) - Overview of options available on cars   
""")

st.markdown("---")
st.subheader("Dataset Preview")
# Run the below code if the check is checked
if st.checkbox("Show processed data"):
    st.subheader("Overview of 10 random rows")
    st.write(dataset_price.sample(10))
st.markdown("""
    The dataset was given by the company. We made some adapations in order to facilitate the present analysis,
    but also the following building of a machine learning model in order to predict the rental price per day of a car.
""")

col1, col2 = st.columns(2)

with col1:
    # Graph 1
    st.markdown("---")
    st.subheader("plot 1")
    st.markdown("### Mean rental price per day ")
    fig1 = go.Figure(go.Indicator(mode = "gauge+number",
                                  value = dataset_price["rental_price_per_day"].mean(),
                                  domain = {"x": [0, 1], "y": [0, 1]},
                                  gauge={"axis" : {"range" : [None,300]}}
                                  ))
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("""
        The mean price is around 121 euros.
    """)

with col2:
    st.markdown("---")
    st.subheader("plot 2")
    st.markdown("### Evolution of mean price according to the options")
    feature_name = ["GPS","Air conditioning","Private parking available","Automatic car","Getaround connect","Speed regulator","Winter tires"]
    fig2 = go.Figure(data=[go.Bar(y=feature_name,
                                  x =[dataset_price.loc[dataset_price.has_gps==True,"rental_price_per_day"].mean(),
                                      dataset_price.loc[dataset_price.has_air_conditioning==True,"rental_price_per_day"].mean(),
                                      dataset_price.loc[dataset_price.private_parking_available==True,"rental_price_per_day"].mean(),
                                      dataset_price.loc[dataset_price.automatic_car==True,"rental_price_per_day"].mean(),
                                      dataset_price.loc[dataset_price.has_getaround_connect==True,"rental_price_per_day"].mean(),
                                      dataset_price.loc[dataset_price.has_speed_regulator==True,"rental_price_per_day"].mean(),
                                      dataset_price.loc[dataset_price.winter_tires==True,"rental_price_per_day"].mean()],
                                  orientation ="h",
                                  name="True")])
    fig2.update_layout(bargap=0.5, width=1000, height=400)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("""
        Some options allow us to increase the price of renting a car for the day.
        """)

# Graph 3
st.markdown("---")
st.subheader("plot 3")
st.markdown("### Type of models rented according to the kind of fuel")
fig3 = px.histogram(dataset_price,
                   x= "model_key_clean",
                   color="fuel",
                   width=1000,
                   labels={"model_key_clean" : "model"}
                   )
st.plotly_chart(fig3, use_container_width=True)
st.markdown("""
    Some car brands are more represented. In parralel, we can see that diesel is still the main kind of fuel used.
""")

# Graph 4
st.markdown("---")
st.subheader("plot 4")
st.markdown("### Overview of options available on cars")
L= len(dataset_price)
feature_name = ["GPS","Air conditioning","Private parking available","Automatic car","Getaround connect","Speed regulator","Winter tires"]
fig4 = go.Figure(data=[go.Bar(x=feature_name, 
                              y =[dataset_price["has_gps"].sum()/L,
                                  dataset_price["has_air_conditioning"].sum()/L, 
                                  dataset_price["private_parking_available"].sum()/L,
                                  dataset_price["automatic_car"].sum()/L,
                                  dataset_price["has_getaround_connect"].sum()/L,
                                  dataset_price["has_speed_regulator"].sum()/L,
                                  dataset_price["winter_tires"].sum()/L],
                              name="True"),
                       go.Bar(x=feature_name, 
                              y =[1-dataset_price["has_gps"].sum()/L,
                                  1-dataset_price["has_air_conditioning"].sum()/L,
                                  1-dataset_price["private_parking_available"].sum()/L,
                                  1-dataset_price["automatic_car"].sum()/L,
                                  1-dataset_price["has_getaround_connect"].sum()/L,
                                  1-dataset_price["has_speed_regulator"].sum()/L,
                                  1-dataset_price["winter_tires"].sum()/L],
                              name="False")])
fig4.update_layout(barmode="stack", bargap=0.07, height=400)
st.plotly_chart(fig4, use_container_width=True)
st.markdown("""
    Some options are very usual in cars as GPS and winter tires.
    Private parking and getarount connect can be found once in two.
    Finally, air conditionning, automatic car and speed regulator are less common.
""")

# Footer
empty_space, footer = st.columns([1, 2])

with empty_space:
    st.write("")

with footer:
    st.markdown("""
        [my Github](www.github.com/sdupland)
    """)
