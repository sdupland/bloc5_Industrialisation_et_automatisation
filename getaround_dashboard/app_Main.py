import streamlit as st

# Config
st.set_page_config(
    page_title="Getaround Data analysis",
    layout="wide"
)

# App
st.title('Getaround Data analysis - Dashboard')
st.write("")

# Loading Text
st.markdown("""
    [Getaround](https://fr.getaround.com/) is a leading car sharing platform in Europe.
    The application allows users to book a car for a specific time period (from hours to days).
    Drivers need to bring back the car on time but it happens that drivers are late for the checkout.
    This situation may generate problems if the car is reserved on a short time after the return.
    
    It results in two main issues :
    - the next customer has to wait for the car returning back, which generates negative feedback from them
    - the turnover generated can be impacted as the rental period can be shortened, or worse cancelled
    
    The goal of this dashboard is :
    - to give some insights on delays and prices
    - to analyse the impact of introducing a time threshold on rentals.
    Within the time threshold, a car will not be displayed in the search results if the requested checkin or checkout times are very close (depending ont the delay decided).
""")

st.write("")
st.write("")
st.write("")
   
with st.expander("About this app"):
    st.write("This app was made with streamlit.")
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=250)

# Footer
empty_space, footer = st.columns([1, 2])

with empty_space:
    st.write("")

with footer:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.markdown("""
        [my Github](https://github.com/sdupland)
    """)
