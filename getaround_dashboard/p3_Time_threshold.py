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
    max_value=360,
    value=(0),)
st.write("Start time :  {} minutes or around {} hours".format(threshold_time, round(threshold_time/60,1)))
st.markdown("")
mask_rented_before = dataset_threshold["previous_ended_rental_id_category"] != "no_rented_before or delay > 12 hours"
mask_delay = dataset_threshold["state"] == "ended"
mean_price_minutes = 0.084 # calculate during the eda of prices data.
cost_time_thresold = dataset_threshold.loc[mask_delay&mask_rented_before, "time_delta_with_previous_rental_in_minutes"].apply(lambda x : (x-threshold_time)*mean_price_minutes if x<threshold_time else 0).sum()
st.markdown("#### With a time treshold of {} minutes, the loss of turnover will be potentially of around {} euros".format(threshold_time, int(cost_time_thresold)))
st.markdown("""
    This calcul is based on the following approach.
    
    On the current situation, some customers are late in their checkin. In this case, if the time delta between two rentals is less important than the time delay, the next customer won't be able to rent the car on the scheduled time.
    It is a direct loss of turnover for our company (we assume that customers which are waiting for their cars don't pay even if their rental period has begun, and also they don't shift their rental period). 
    
    if we choose to set up a time treshold, we could possibly lose a part of our turnover because next customers won't be able to rent a car too close form the previous one.
    One the one hand, when there is a delay and an insufficient period of time betwen two rentals, there is already a loss of turnover as we saw above. So the financial impact is neutral.
    On another side, in cases where there is no delay for example, we will loss a part of our turnover.
    
    Based on historical data, and according to the period of time we select, we can calculate the quantity of minutes that won't be rented because of the time threshold (we assume that customers won't just shift their rental period).
    We don't see any direct financial gain to set up a time threshold.
    
    That's why our calculations of impact are always negative in our approach. We have already observed a loss of turnover.
    So set up a time threshold won't help us to recover directly this turnover because the time threshold will lead to a loss of turnover too :
    - on cases where there were no issue, we rented a car before and now it won't be the case.
    - on cases where there were issues, we didn't rent a car because of the delay. We replace the loss of turnover du to delay from the one due to the time threshold.
    
    But this approach has some limitations we will see in conclusion.
""")

# Plot 6
st.markdown("---")
st.subheader("Plot 6")
st.markdown("### Conclusion")
st.markdown("")
st.markdown("""
    Our approach which is perhaps suprising needs to be balanced by different points :
    - we don't know the origin of cancellation and they can be linked to delay. this point should be taking account in our calculation
    - we don't know also how customers can adapt to a time threshold. Perhaps they will just shift the period of location for example
    - we aren't taking account the customer's satisfaction (or dissatisfaction !) for which we don't have information. We can't measure it in financial terms for example.
    
    In terms of recommendations, we will say that the previous calculation must be put into perspective with the customer's satisfaction and the limitations mentioned.
    We should investigate on different ways to improve this work and for example :
    - lead a satisfaction survey to measure the impact of delay on customer's beahaviour,
    - clarify the origin of cancelation.
    
    Nevertheless, on this first basis, we can :
    - evaluate a financial impact of a time threshold,
    - measure its importance in view of the size of the company, its turnover, and its goal in terms of customer service.
""")

# Footer
empty_space, footer = st.columns([1, 2])

with empty_space:
    st.write("")

with footer:
    st.markdown("""
        [my Github](www.github.com/sdupland)
    """)
