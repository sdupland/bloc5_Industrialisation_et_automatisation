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
st.title("Time threshold analysis")

# Loading Image and Text
st.markdown("""
    A time threshold should be a way to avoid customer disagreament, or the cancellation of next rental, due to late return of the precedent location.
    In addition, this issue appears when the gap time between two rentals is shorter than the delay.
    We will try first to identify in the given dataset these situations.
""")

@st.cache_data()
def load_data():
    path = "data/dataset_delay_threshold.csv"
    data = pd.read_csv(path)
    return data

dataset_threshold = load_data()

# Content
st.sidebar.header("Table of content")
st.sidebar.markdown("""
    * [Preview of data set](#dataset-preview)
    * [Plot 1](#plot-1) - Average time delta in minutes when insufficient
    * [Plot 2](#plot-2) - Median time delta in minutes when insufficient
    * [Plot 3](#plot-3) - Distribution of time delta when negative
    * [Plot 4](#plot-4) - How long was late the last driver if there is a lack of time between two rentals
    * [Plot 5](#plot-5) - Impact of a time threshold of your choice
    * [Plot 6](#plot-6) - Conclusion
""")

st.markdown("---")
st.subheader("Dataset Preview")
# Run the below code if the check is checked
if st.checkbox("Show processed data"):
    st.subheader("Overview of 10 random rows")
    st.write(dataset_threshold.sample(10))
st.markdown("""
    The dataset was given by the company. We made some adapations in order to facilitate the present analysis,
    but also the following building of a machine learning model in order to predict the rental price per day of a car.
""")

col1, col2 = st.columns(2)

with col1:
    # Plot 1
    st.markdown("---")
    st.subheader("Plot 1")
    st.markdown("### Average time delta in minutes when insufficient")
    mean_time_delta = dataset_threshold.loc[dataset_threshold["time_delta"]<0,"time_delta"].mean()
    fig1 = go.Figure(go.Indicator(mode = "gauge+number",
                                  value = mean_time_delta,
                                  domain = {"x": [0, 1], "y": [0, 1]},
                                  gauge={"axis" : {"range" : [None,dataset_threshold["time_delta"].min()]}}
                                  ))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Plot 2
    st.markdown("---")
    st.subheader("Plot 2")
    st.markdown("### Median time delta in minutes when insufficient")
    median_time_delta = dataset_threshold.loc[dataset_threshold["time_delta"]<0,"time_delta"].median()
    fig2 = go.Figure(go.Indicator(mode = "gauge+number",
                                  value = median_time_delta,
                                  domain = {"x": [0, 1], "y": [0, 1]},
                                  gauge={"axis" : {"range" : [None,dataset_threshold["time_delta"].min()]}}
                                  ))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
    The time delta indicator is the difference between :
    - the time available between the last and next rental car, if applicable,
    - the time of delay if applicable
    
    A negative value in the dataset means that delay of the last checkin was bigger than the time available between the next rental car.
    This is the issue we have to manage.
    At the opposite, a positive value in the dataset shows that there is no problem for the next driver, even if the last one was late.
    
    We can see a significant difference between mean and median, due to outliers.
""")

# Plot 3
st.markdown("---")
st.subheader("Plot 3")
st.markdown("### Distribution of time delta when negative")
fig3 = px.histogram(dataset_threshold,
                   x=dataset_threshold.loc[dataset_threshold["time_delta"]<0,"time_delta"],
                   labels={"time_delta":"time delta"},
                   nbins=20
                   )
st.plotly_chart(fig3, use_container_width=True)
st.markdown("""
    The distribution confirms the wide range of value with some outliers linked to unusual delays.
""")

# Plot 4
st.markdown("---")
st.subheader("Plot 4")
st.markdown("### How long was late the last driver if there is a lack of time between two rentals")
fig4 = px.pie(dataset_threshold.loc[dataset_threshold["time_delta_cat"]=="lack of time between two rentals"],
              names="delay_slices",
              labels={"time_delta_cat":"time delta"},
              category_orders=dict(delay_slices=["Delay <= 10 mins", "10 <= Delay <= 30 mins", "30 mins < Delay <= 1 hour", "1 hour < Delay <= 2 hours", "2 hours < Delay <= 4 hours", "Delay > 4 hours"])
              )
st.plotly_chart(fig4, use_container_width=True)
st.markdown("""
    Below some figures to resume :
    - Until 1 hour of delay = 34,7%
    - between 1 and two hours = 20,7%
    - more than two hours = 44,4%
""")

# Plot 5
st.markdown("---")
st.subheader("Plot 5")
st.markdown("### Impact of a time threshold of your choice")
threshold_time = st.slider(
    "Which time threshold do you want to choose, in minutes ?",
    min_value=0,
    max_value=240,
    value=(0),)
st.write("Start time :  {} minutes or around {} hours".format(threshold_time, round(threshold_time/60,1)))
st.markdown("")
mask_rented_before = dataset_threshold["previous_ended_rental_id_category"] != "no_rented_before or delay > 12 hours"
mask_delay = dataset_threshold["state"] == "ended"
mean_price_minutes = 0.084 # calculate during the eda of prices data.
cost_time_thresold = dataset_threshold.loc[mask_delay&mask_rented_before, "time_delta_with_previous_rental_in_minutes"].apply(lambda x : (x-threshold_time)*mean_price_minutes if x<threshold_time else 0).sum()
st.markdown("#### With a time treshold of {} minutes, the loss of turnover will be potentially of around {} euros".format(threshold_time, int(cost_time_thresold)))

# Plot 6
st.markdown("---")
st.subheader("Plot 6")
st.markdown("### Conclusion")
st.markdown("")
st.markdown("""
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
""")

# Footer
empty_space, footer = st.columns([1, 2])

with empty_space:
    st.write("")

with footer:
    st.markdown("""
        [my Github](www.github.com/sdupland)
    """)
