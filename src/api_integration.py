import requests
import os
from dotenv import load_dotenv

load_dotenv()

YELP_API_KEY = os.getenv("YELP_API_KEY")

def fetch_yelp_data(location, term):
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    params = {"location": location, "term": term, "limit": 5}
    response = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return None

if __name__ == '__main__':
    print(fetch_yelp_data("San Francisco", "Pizza"))# Placeholder for api_integration.py