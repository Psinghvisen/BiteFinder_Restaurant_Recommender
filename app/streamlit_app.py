import streamlit as st
from src.recommendation_engine import recommend_restaurants

st.title("BiteFinder")
location = st.text_input("Enter Location")
cuisine = st.text_input("Enter Cuisine")
rating = st.slider("Select Minimum Rating", 1.0, 5.0, 4.0)

if st.button("Find Restaurants"):
    recommendations = recommend_restaurants(location, cuisine, rating)
    st.write(recommendations)
