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
st.title("Delay analysis")

# use to cache function that return data from a csv file
# function is run and data stores in memory for after
@st.cache_data()
def load_data():
    path = "data/dataset_delay_clean.csv"
    data = pd.read_csv(path)
    return data

dataset_delay = load_data()

# Content of this page, on sidebar
st.sidebar.header("Table of content")
st.sidebar.markdown("""
    * [Preview of data set](#dataset-preview)
    * [Graph 1](#plot-1) - How is ordered our cars
    * [Graph 2](#plot-2) - When is returned our cars
    * [Graph 3](#plot-3) - Which Rate of cancellation
    * [Graph 4](#plot-4) - Are the cars rented before
    * [Graph 5](#plot-5) - Check in status according to the situation of the car previously (rented or not)
    * [Graph 6](#plot-6) - Check in status according to the checkin type
    * [Graph 7](#plot-7) - Distribution of delay according to different slices
""")

# see a sample of 10 rows of the dataset if the check is checked
st.markdown("---")
st.subheader("Dataset Preview")
# Run the below code if the check is checked
if st.checkbox("Show processed data"):
    st.subheader("Overview of 10 random rows")
    st.write(dataset_delay.sample(10))
st.markdown("""
    The dataset was given by the company. We made some adapations in order to facilitate the present analysis,
    but also the following building of a machine learning model in order to predict the rental price per day of a car.
""")

# allow to separate the page in two columns in orderto present two graphs for example
col1, col2 = st.columns(2)

# firt column
with col1:
    # Graph 1
    st.markdown("---")
    st.subheader("plot 1")
    st.markdown("### how is ordered our cars")
    fig1 = px.pie(dataset_delay,
                  names="checkin_type",
                  hole=.5)
    fig1.update_layout(showlegend=False)
    fig1.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("""
        The main way of renting our car is throuhg a meeting between the owner and the driver (mobile).
        Then comes a full digital way where people doesn"t meet each other (connect). Paper is no longer used.
    """)

# second column
with col2:
    # Graph 2
    st.markdown("---")
    st.subheader("plot 2")
    st.markdown("### When is return our cars")
    fig4 = px.pie(dataset_delay.loc[dataset_delay.state=="ended",:],
                  names="delay_status",
                  hole=.5)
    fig4.update_traces(textposition="inside", textinfo="percent+label")
    fig4.update_layout(showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("""
        More than 52% of cars are returned with delay which is the very high rate.
        We"ll have a look more precisely on delays in the following graph.
    """)

col1, col2 = st.columns(2)

with col1:    
    # Graph 3
    st.markdown("---")
    st.subheader("plot 3")
    st.markdown("### Rate of cancellation")
    canceled_number = dataset_delay.loc[dataset_delay["state"]=="canceled","state"].count()
    fig3 = go.Figure(go.Indicator(mode = "gauge+number",
                                  value = canceled_number/len(dataset_delay.state)*100,
                                  domain = {"x": [0, 1], "y": [0, 1]},
                                  gauge={"axis" : {"range" : [None,100]}}
                                  ))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("""
        The cancellation rate at around 15% is quite high.
        We don"t have the infomation about the reasons which could be very helpful.
    """)

with col2:
    # Graph 4
    st.markdown("---")
    st.subheader("plot 4")
    st.markdown("### Are the cars rented before")
    fig4 = px.pie(dataset_delay,
                  names="previous_ended_rental_id_category",
                  hole=.5)
    fig4.update_traces(textposition="inside", textinfo="percent+label")
    fig4.update_layout(showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("""
        Only 8,6% of the cars have been rented before the next location.
    """)

# Graph 5
st.markdown("---")
st.subheader("plot 5")
st.markdown("### Check in status according to the previously situation of the car (rented or not)")
fig5 = px.histogram(dataset_delay,
                    color= "delay_status",
                    x="previous_ended_rental_id_category",
                    labels={"delay_status" : "delay status", "previous_ended_rental_id_category" : "Car rented previously"}) # used to present clean label of data
st.plotly_chart(fig5, use_container_width=True)
st.markdown("""
    There is no real correlation betwenn these two variables.
    """)

# Graph 6
st.markdown("---")
st.subheader("plot 6")
st.markdown("### Check in status according to the checkin type")
fig5 = px.histogram(dataset_delay,
                    x= "delay_status",
                    color="checkin_type",
                    labels={"delay_status" : "delay status", "checkin_type" : "checkin type"})
st.plotly_chart(fig5, use_container_width=True)
st.markdown("""
    Proportionately speaking, people who rented a car using the connect way seems to return it on time or in advance more frequently.
    Nevertheless, the differencce is not really significant.
    """)

# Graph 7
st.markdown("---")
st.subheader("plot 7")
st.markdown("### Distribution of delay according to different slices")
fig6 = px.histogram(dataset_delay.loc[dataset_delay.delay_status=="delayed",:],
                    x= "delay_slices",
                    labels={"delay_slices" : "delay slices"},
                    # allow to choose the correct order of the differents categories
                    category_orders=dict(delay_slices=["Delay <= 10 mins", "10 <= Delay <= 30 mins", "30 mins < Delay <= 1 hour", "1 hour < Delay <= 2 hours", "2 hours < Delay <= 4 hours", "Delay > 4 hours"]),
                    histnorm="percent") # select the type of data used for y axis
st.plotly_chart(fig6, use_container_width=True)
st.markdown("""
    The range of delays is very important, from a few minutes to a day !
    About 30% percent of delays are less than 30 minutes, and 47% less than 1 hour.
    At the opposite, a little less than 15% of people have returned the car with more than 4 hours of delay.
    """)

# Footer
empty_space, footer = st.columns([1, 2])

with empty_space:
    st.write("")

with footer:
    st.markdown("""
        [my Github](www.github.com/sdupland)
    """)
