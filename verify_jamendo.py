import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("JAMENDO_CLIENT_ID")

def search_jamendo_by_mood(mood="chillout"):
    """Searches Jamendo for tracks with specific mood tags."""
    # Updated to v3.0 as per latest documentation
    url = "https://api.jamendo.com/v3.0/tracks/"
    params = {
        "client_id": CLIENT_ID,
        "format": "json",
        "limit": 5,
        "fuzzytags": mood,  # fuzzytags is common in v3.0 for mood search
        "order": "popularity_total",
        "include": "musicinfo" # To get more details if needed
    }
    
    print(f"Attempting to connect to Jamendo v3.0 with Client ID: {CLIENT_ID}...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        headers = data.get("headers", {})
        print(f"Status: {headers.get('status')} | Results Count: {headers.get('results_count')}")
        
        if headers.get("status") != "success":
            print(f"Jamendo Warning: {headers.get('error_message')}")

        tracks = data.get("results", [])
        if not tracks:
            print(f"No tracks found for '{mood}'. Trying 'rock'...")
            params["fuzzytags"] = "rock"
            response = requests.get(url, params=params)
            tracks = response.json().get("results", [])

        print(f"--- Jamendo Results ---")
        for i, track in enumerate(tracks, 1):
            print(f"{i}. {track['name']} by {track['artist_name']}")
            print(f"   Preview: {track['audio']}")
    else:
        print(f"HTTP Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    if not CLIENT_ID or CLIENT_ID == "your_jamendo_client_id":
        print("1. Go to https://developer.jamendo.com/v1.0/signup")
        print("2. Create a free account and copy your 'Client ID'.")
        print("3. Paste it into your .env file as JAMENDO_CLIENT_ID.")
    else:
        search_jamendo_by_mood("chill")
