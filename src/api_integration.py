import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve Google Maps API Key from .env file
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def fetch_geocode(address):
    """
    Fetches geocoding data (latitude, longitude) from Google Maps Geocoding API.

    Args:
        address (str): The address to geocode.

    Returns:
        dict: A dictionary containing latitude and longitude, or None if the request fails.
    """
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": GOOGLE_MAPS_API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching geocode: {response.status_code}, {response.text}")
        return None


def calculate_distance(origin, destination):
    """
    Calculates the distance and travel time between two locations using Google Maps Distance Matrix API.

    Args:
        origin (str): The starting location (e.g., "San Francisco").
        destination (str): The destination location (e.g., "Los Angeles").

    Returns:
        dict: A dictionary containing distance and duration, or None if the request fails.
    """
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "key": GOOGLE_MAPS_API_KEY,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching distance: {response.status_code}, {response.text}")
        return None


if __name__ == "__main__":
    # Test Geocoding API
    address = "1600 Amphitheatre Parkway, Mountain View, CA"
    geocode_result = fetch_geocode(address)
    if geocode_result:
        location = geocode_result["results"][0]["geometry"]["location"]
        print(
            f"Geocoding Result:\nLatitude: {location['lat']}, Longitude: {location['lng']}"
        )

    # Test Distance Matrix API
    origin = "San Francisco, CA"
    destination = "Los Angeles, CA"
    distance_result = calculate_distance(origin, destination)
    if distance_result:
        distance = distance_result["rows"][0]["elements"][0]["distance"]["text"]
        duration = distance_result["rows"][0]["elements"][0]["duration"]["text"]
        print(f"Distance Matrix Result:\nDistance: {distance}, Travel Time: {duration}")
