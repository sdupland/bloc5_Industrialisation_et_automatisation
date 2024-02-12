import streamlit as st
import requests


# Config
st.set_page_config(
    page_title="Getaround Data analysis",
    layout="wide"
)

# App
st.title("API call")

# Loading Image and Text
st.markdown("""
    According to different characteristic, you will get a rental price estimation.
""")

# Content
st.sidebar.markdown("")
state_button = st.sidebar.button("Launch to get the price estimation")
st.sidebar.markdown("")
st.sidebar.markdown("")


st.markdown("---")
st.markdown("")
option_model = st.selectbox("Which models do you want to use ?",
                                    ("Citroën","Renault","BMW","Peugeot","Audi","Nissan","Mitsubishi","Mercedes","Volkswagen","Toyota","others","SEAT","Subaru","PGO","Opel","Ferrari"),
                                    index=None,
                                    placeholder="Choose an option")
st.markdown("")
st.markdown("---")
st.markdown("")
option_fuel = st.selectbox("What kind of fuel do you want ?",
                                    ("diesel","petrol","others"),
                                    index=None,
                                    placeholder="Choose an option")
st.markdown("")
st.markdown("---")
st.markdown("")
option_color = st.selectbox("What kind of car's color do you want ?",
                                    ("black","grey","blue","white","brown","silver","red","beige","others"),
                                    index=None,
                                    placeholder="Choose an option")
st.markdown("")
st.markdown("---")
st.markdown("")
option_car_type = st.selectbox("Which car type do you want ?",
                                    ("convertible","coupe","estate","sedan","suv","subcompact","hatchback","van"),
                                    index=None,
                                    placeholder="Choose an option")
st.markdown("")
st.markdown("---")
st.markdown("")
option_engine_power = st.slider(
    "Which engine power do you want to choose ?",
    min_value=0,
    max_value=300,
    value=(0),) # default value
st.markdown("")
st.markdown("---")
st.markdown("")
option_mileage = st.slider(
    "Which mileage do you want ?",
    min_value=0,
    max_value=100000,
    value=(0),) # default value
st.markdown("")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1 :
    st.markdown("")
    option_gps = st.checkbox("Has GPS ?", value=False)
    st.markdown("")
    st.markdown("---")
    st.markdown("")

with col2 :
    st.markdown("")
    option_automatic = st.checkbox("Automatic car ?", value=False)
    st.markdown("")
    st.markdown("---")
    st.markdown("")

with col3 :
    st.markdown("")
    option_parking = st.checkbox("Private parking ?", value=False)
    st.markdown("")
    st.markdown("---")
    st.markdown("")
    
with col4 :
    st.markdown("")
    option_air_conditionning = st.checkbox("Air conditionning ?", value=False)
    st.markdown("")
    st.markdown("---")
    st.markdown("")

col1, col2, col3, col4 = st.columns(4)

with col1 :
    st.markdown("")
    option_speed = st.checkbox("Speed regulator ?", value=False)
    st.markdown("")
    st.markdown("---")
    st.markdown("")

with col2 :
    st.markdown("")
    option_tires = st.checkbox("Winter tires ?", value=False)
    st.markdown("")
    st.markdown("---")
    st.markdown("")

with col3 :
    st.markdown("")
    option_getaround = st.checkbox("Getaround connect ?", value=False)
    st.markdown("")
    st.markdown("---")
    st.markdown("")

with col4 :
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    
# dictionary with all the charasteristics of our car and a set of values we want
payload = {
    "model_key": option_model,  
    "mileage": option_mileage,  
    "engine_power": option_engine_power,  
    "fuel": option_fuel,  
    "paint_color": option_color,  
    "car_type": option_car_type,  
    "private_parking_available": option_parking,  
    "has_gps": option_gps,  
    "has_air_conditioning": option_air_conditionning,  
    "automatic_car": option_automatic,  
    "has_getaround_connect": True,  
    "has_speed_regulator": option_speed,  
    "winter_tires": option_tires  
}

# request used when api is deployed on heroku
if state_button :
    r = requests.post("https://getaround-api-sndd-b23920c55a69.herokuapp.com/predict", json=payload).json()
    st.sidebar.markdown("Predicted rental price per day in dollars :")
    st.sidebar.markdown(r["Predicted rental price per day in dollars"])

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
