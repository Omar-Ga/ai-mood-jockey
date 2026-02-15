import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_spotify_token():
    """Retrieves an access token using Client Credentials Flow."""
    auth_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(auth_url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Error fetching token: {response.status_code}")
        print(response.json())
        return None

def search_test_songs(token, query="Lofi"):
    """Searches for songs and prints the first 5 results."""
    search_url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": query,
        "type": "track",
        "limit": 5
    }
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        tracks = response.json().get("tracks", {}).get("items", [])
        print(f"--- Top 5 results for '{query}' ---")
        for i, track in enumerate(tracks, 1):
            artists = ", ".join([artist["name"] for artist in track["artists"]])
            print(f"{i}. {track['name']} by {artists}")
    else:
        print(f"Error searching tracks: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    if not CLIENT_ID or not CLIENT_SECRET or CLIENT_ID == "your_spotify_client_id":
        print("Please update your .env file with real Spotify API credentials.")
    else:
        token = get_spotify_token()
        if token:
            search_test_songs(token)
