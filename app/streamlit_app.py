import sys
import os

# Add the parent directory of the current file to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.recommendation_engine import top_five_restaurants
from src.api_integration import fetch_geocode, calculate_distance


# Add heatmap function
def create_heatmap(data):
    """
    Create a heatmap using Plotly Express for restaurant ratings.

    Args:
        data (pd.DataFrame): DataFrame with latitude, longitude, and rating.
    Returns:
        Plotly figure object
    """
    fig = px.density_mapbox(
        data,
        lat="latitude",
        lon="longitude",
        z="rating",
        radius=10,
        center=dict(lat=37.7749, lon=-122.4194),
        zoom=10,
        mapbox_style="stamen-terrain",
        title="Restaurant Heatmap Based on Ratings",
    )
    return fig


# Title of the app
st.markdown(
    """
    <h1 style='text-align: center; color: #FF5733; font-family: Arial;'>
        🍽️ BiteFinder: A Personalized Dining Guide 🍽️
    </h1>
    """,
    unsafe_allow_html=True,
)

# Sidebar for inputs
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2649/2649082.png", width=200)
st.sidebar.header("Filter Your Search 🔍")
user_location = st.sidebar.text_input("📍 Enter Your Location")
cuisine = st.sidebar.text_input("🍴 Enter Cuisine Type")
rating = st.sidebar.slider("⭐ Select Minimum Rating", 1.0, 5.0, 4.0)

# Heatmap option
show_heatmap = st.sidebar.checkbox("Show Heatmap of Restaurants")

# Action Button
if st.sidebar.button("Find Restaurants"):
    try:
        # Load the dataset
        data = pd.read_csv("../data/final_combined_cleaned_data.csv")

        # Apply filtering
        filtered_data = data[
            (data["address"].str.contains(user_location, case=False, na=False))
            & (data["cuisine_type"].str.contains(cuisine, case=False, na=False))
            & (data["rating"] >= rating)
        ]

        # Top 5 results if filters are empty
        if user_location == "" and cuisine == "":
            st.subheader("🍽️ Top 5 Restaurants Based on Ratings")
            recommendations = top_five_restaurants()
        else:
            st.subheader("🍽️ Top 5 Restaurants Matching Your Filters")
            recommendations = filtered_data.nlargest(5, "rating")

        # Display recommendations
        if not recommendations.empty:
            for _, row in recommendations.iterrows():
                st.markdown(
                    f"""
                    <div style='border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin: 10px 0; 
                                box-shadow: 2px 2px 12px #aaa; background-color: #fdfdfd;'>
                        <h3 style='color: #FF5733; font-family: Arial;'>🍴 {row['name']}</h3>
                        <p><b>📍 Address:</b> {row['address']}</p>
                        <p><b>🍽️ Cuisine:</b> {row['cuisine_type']}</p>
                        <p><b>⭐ Rating:</b> {row['rating']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.warning("No matching restaurants found. Try changing your filters.")

        # Display Heatmap
        if show_heatmap:
            st.subheader("🌍 Heatmap of Restaurant Ratings")
            fig = create_heatmap(data)
            st.plotly_chart(fig, use_container_width=True)

    except FileNotFoundError:
        st.error(
            "Error: The cleaned dataset file is missing. Run data preparation first."
        )
    except KeyError as e:
        st.error(f"Error: Missing column - {e}")

# Footer
st.write("---")
st.write("BiteFinder | A Personalized Guide to Dine | Powered by Streamlit and Plotly")
