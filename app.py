import streamlit as st
import pandas as pd
import os
import geopy
import google.generativeai as genai
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
import datetime

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Function to get data from Gemini API
def get_data_from_gemini(requirements):
    response = model.generate_content(requirements)
    return response.text


# Streamlit page layout
st.title('📍🏖️ Craft Your Journey ✈️')
st.markdown("""
🎈 Embark on your next great adventure with us! Let's craft a travel experience that's as unique as you are. Welcome to your gateway to the world.
""")

# Sidebar for user input
with st.sidebar:
    st.header("Fill in Your Travel Information")
    destination = st.text_input("Destination", "e.g., Paris")
    num_people = st.number_input("Number of People", min_value=1, value=2)
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    # Budget input as both slider and text input for precise control
    budget_slider = st.slider("Budget (USD)", 500, 10000, 1500)
    budget_input = st.text_input("Or Enter Exact Budget", str(budget_slider))
    activity_level = st.selectbox("Activity Level", ["Low (Relaxing)", "Medium (Moderate Exploring)", "High (Adventurous)"])
    experience_types = st.multiselect("Experience Type", ["Cultural (Arts, History)", "Natural (Outdoors, Wildlife)", "Gastronomic (Food, Drinks)", "Recreational (Leisure, Shopping)"])
    personal_notes = st.text_area("Notes or Keywords", "Type your notes or specific interests here...")

# Main content area
if st.button('Generate Travel Plan', key='plan_button'):
    requirements = f"""
    Please create a travel plan for {num_people} people. Destination: {destination}, from {start_date} to {end_date}, with a budget of {budget_input} USD. Activity Level: {activity_level}, Experience Types: {', '.join(experience_types)}, Notes: {personal_notes}.
    """
    response = model.generate_content(requirements)
    if response.text:
        st.subheader("Your Travel Plan")
        st.write(response.text)
    else:
        st.error("Failed to generate a travel plan, please check your input or try again later.")
    st.write("")  # Add a space for better separation

# Geocoding with Geopy
geolocator = Nominatim(user_agent="travel_planner")
location = geolocator.geocode(destination)
if location:
    # Add extra space before the map
    st.write("##")  # Markdown for spacing
    st.map(data=pd.DataFrame({'lat': [location.latitude], 'lon': [location.longitude]}), zoom=11, use_container_width=True)
else:
    st.error("Unable to find the specified location, please try different search terms.")
