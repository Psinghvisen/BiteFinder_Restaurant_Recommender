import sys
import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Add the parent directory of the current file to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.recommendation_engine import top_five_restaurants

# Load environment variables (Google Maps API Key)
load_dotenv("../.env")
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

if GOOGLE_MAPS_API_KEY is None:
    print("Error: GOOGLE_MAPS_API_KEY not found.")
else:
    print("GOOGLE_MAPS_API_KEY loaded successfully.")


# Function to create Google Static Maps URL
def generate_google_maps_url(lat, lon):
    """
    Generate a Google Maps Static API URL for a given latitude and longitude.
    """
    return f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=15&size=600x400&markers=color:red%7C{lat},{lon}&key={GOOGLE_MAPS_API_KEY}"


# Function to create a Google Maps Navigation URL
def generate_google_maps_navigation_url(lat, lon):
    """
    Generate a Google Maps URL for navigation to a location from the user's current location.
    """
    return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}&travelmode=driving"


# Title of the app
st.title("🍽️ BiteFinder: A Personalized Dining Guide 🍽️")

# Sidebar for user inputs
st.sidebar.header("Filter Your Search 🔍")
user_location = st.sidebar.text_input("📍 Enter Your Location")
cuisine = st.sidebar.text_input("🍴 Enter Cuisine Type")
rating = st.sidebar.slider("⭐ Select Minimum Rating", 1.0, 5.0, 4.0)

# Action Button
if st.sidebar.button("Find Restaurants"):
    try:
        # Load the cleaned dataset
        data = pd.read_csv("../data/final_combined_cleaned_data.csv")

        # Apply filtering
        filtered_data = data[
            (data["city"].str.contains(user_location, case=False, na=False))
            & (data["cuisine_type"].str.contains(cuisine, case=False, na=False))
            & (data["rating"] >= rating)
        ]

        # If no results are found
        if filtered_data.empty:
            st.warning("No matching restaurants found. Try changing your filters.")
        else:
            st.subheader("🍴 Top 5 Restaurants Matching Your Filters")

            # Display restaurant details and clickable navigation link
            for _, row in filtered_data.nlargest(5, "rating").iterrows():
                st.markdown(
                    f"""
                    **Name:** {row['name']}  
                    **Address:** {row['address']}  
                    **Cuisine:** {row['cuisine_type']}  
                    **Rating:** {row['rating']}
                    """
                )

                # Generate and display the Google Static Map
                google_maps_url = generate_google_maps_url(
                    row["latitude"], row["longitude"]
                )
                st.image(
                    google_maps_url,
                    caption=f"Location: {row['name']}",
                    use_column_width=True,
                )

                # Generate a clickable Google Maps Navigation link
                navigation_url = generate_google_maps_navigation_url(
                    row["latitude"], row["longitude"]
                )
                st.markdown(
                    f"[🚗 Navigate to {row['name']}](<{navigation_url}>)",
                    unsafe_allow_html=True,
                )

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Footer
st.write("---")
st.write(
    "BiteFinder | A Personalized Guide to Dine | Powered by Google Maps and Streamlit"
)
