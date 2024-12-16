import sys
import os
import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv

# Add the parent directory of the current file to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load environment variables
load_dotenv("../.env")
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

if not GOOGLE_PLACES_API_KEY:
    st.error("⚠️ Google Places API Key not found. Please check your .env file.")
    st.stop()


# Function to fetch restaurants from Google Places API
def fetch_restaurants(location, keyword, min_rating=4.0, max_results=5):
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{keyword} restaurants in {location}",
        "key": GOOGLE_PLACES_API_KEY,
    }
    response = requests.get(base_url, params=params)
    results = response.json()
    restaurants = []

    if "results" in results:
        for place in results["results"]:
            rating = place.get("rating", 0)
            if rating >= min_rating:
                restaurants.append(
                    {
                        "name": place["name"],
                        "address": place.get("formatted_address", "N/A"),
                        "rating": rating,
                        "latitude": place["geometry"]["location"]["lat"],
                        "longitude": place["geometry"]["location"]["lng"],
                    }
                )
            if len(restaurants) >= max_results:
                break
    return restaurants


# Function to generate Google Static Map URL
def generate_google_maps_url(lat, lon):
    return f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=15&size=600x400&markers=color:red%7C{lat},{lon}&key={GOOGLE_PLACES_API_KEY}"


# Function to generate a combined map with multiple markers
def generate_combined_google_maps_url(restaurants):
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    marker_list = [
        f"markers=color:red%7Clabel:{idx+1}%7C{restaurant['latitude']},{restaurant['longitude']}"
        for idx, restaurant in enumerate(restaurants)
    ]
    markers = "&".join(marker_list)
    full_url = f"{base_url}{markers}&size=800x400&key={GOOGLE_PLACES_API_KEY}"
    return full_url


# Function to generate navigation URL
def generate_navigation_url(lat, lon):
    return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"


# Custom CSS for Dark Theme
st.markdown(
    """
    <style>
        body {
            background-color: #1e1e1e;
            color: #f5f5f5;
        }
        .st-bb, .st-at {
            color: #e74c3c; /* Red title font */
        }
        .reportview-container {
            background-color: #1e1e1e;
        }
        .sidebar .sidebar-content {
            background-color: #2c2c2c;
        }
        .st-dd, .st-de {
            background-color: #3d3d3d; /* Darker cards */
        }
        .stButton>button {
            background-color: #e74c3c;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit App Title
st.markdown(
    "<h1 style='color: #e74c3c; text-align: center;'>BiteFinder: Real-Time & Static Restaurant Recommendations</h1>",
    unsafe_allow_html=True,
)

# Sidebar with Image
st.sidebar.image("../data/BITEFINDER.jpg", caption="", use_container_width=True)

# Sidebar Inputs
st.sidebar.header("🔍 Filter Your Search")
user_location = st.sidebar.text_input("📍 Enter Your Location")
cuisine = st.sidebar.text_input("🍴 Enter Cuisine Type")
min_rating = st.sidebar.slider("⭐ Minimum Rating", 1.0, 5.0, 4.0)

# Sidebar Tabs
st.sidebar.subheader("Select Data Source")
tab_selection = st.sidebar.radio("Data Source:", ["Static Data", "Google Places API"])

# Tab 1: Static Data
if tab_selection == "Static Data":
    st.subheader("📊 Top 5 Restaurants (Static Dataset)")
    if st.sidebar.button("Find Restaurants"):
        try:
            data = pd.read_csv("../data/final_combined_cleaned_data.csv")
            filtered_data = data[
                (data["city"].str.contains(user_location, case=False, na=False))
                & (data["cuisine_type"].str.contains(cuisine, case=False, na=False))
                & (data["rating"] >= min_rating)
            ]

            if filtered_data.empty:
                st.warning("No matching restaurants found. Try different filters.")
            else:
                restaurant_list = []
                for _, row in filtered_data.nlargest(5, "rating").iterrows():
                    restaurant_list.append(
                        {
                            "name": row["name"],
                            "latitude": row["latitude"],
                            "longitude": row["longitude"],
                        }
                    )

                # Display Combined Map
                combined_map_url = generate_combined_google_maps_url(restaurant_list)
                st.subheader("🗺️ Combined Map of Top 5 Restaurants")
                st.image(
                    combined_map_url,
                    caption="All Top 5 Restaurants on a Single Map",
                    use_container_width=True,
                )

                # Display Individual Restaurants
                st.subheader("📍 Individual Restaurant Maps")
                for idx, restaurant in enumerate(restaurant_list, start=1):
                    st.markdown(f"**{idx}. {restaurant['name']}**")
                    static_map = generate_google_maps_url(
                        restaurant["latitude"], restaurant["longitude"]
                    )
                    st.image(
                        static_map,
                        caption=f"Location: {restaurant['name']}",
                        use_container_width=True,
                    )
                    navigation_url = generate_navigation_url(
                        restaurant["latitude"], restaurant["longitude"]
                    )
                    st.markdown(
                        f"[🚗 Navigate to {restaurant['name']}]({navigation_url})",
                        unsafe_allow_html=True,
                    )

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Tab 2: Google Places API
elif tab_selection == "Google Places API":
    st.subheader("🌐 Real-Time Recommendations (Google Places API)")
    if st.sidebar.button("Find Restaurants"):
        if not user_location or not cuisine:
            st.warning("Please enter both location and cuisine type.")
        else:
            with st.spinner("Fetching recommendations..."):
                restaurants = fetch_restaurants(user_location, cuisine, min_rating)
                if not restaurants:
                    st.warning(
                        "No real-time matching restaurants found. Try different filters."
                    )
                else:
                    # Display Combined Map
                    combined_map_url = generate_combined_google_maps_url(restaurants)
                    st.subheader("🗺️ Combined Map of Top 5 Restaurants")
                    st.image(
                        combined_map_url,
                        caption="All Top 5 Restaurants on a Single Map",
                        use_container_width=True,
                    )

                    # Display Individual Restaurants
                    st.subheader("📍 Individual Restaurant Maps")
                    for idx, restaurant in enumerate(restaurants, start=1):
                        st.markdown(
                            f"**{idx}. {restaurant['name']}** | **Rating:** {restaurant['rating']} ⭐ | **Address:** {restaurant['address']}"
                        )
                        static_map = generate_google_maps_url(
                            restaurant["latitude"], restaurant["longitude"]
                        )
                        st.image(
                            static_map,
                            caption=f"Location: {restaurant['name']}",
                            use_container_width=True,
                        )
                        navigation_url = generate_navigation_url(
                            restaurant["latitude"], restaurant["longitude"]
                        )
                        st.markdown(
                            f"[🚗 Navigate to {restaurant['name']}]({navigation_url})",
                            unsafe_allow_html=True,
                        )

# Footer
st.write("---")
st.write(
    "BiteFinder | A Personalized Dining Guide | Powered by Google Places API & Static Dataset"
)
