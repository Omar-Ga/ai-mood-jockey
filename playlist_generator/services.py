import os
import requests
from dotenv import load_dotenv

load_dotenv()

class JamendoService:
    @staticmethod
    def get_tracks_by_mood(mood, limit=5):
        """
        Fetches tracks from Jamendo API based on a mood/tag.
        """
        client_id = os.getenv("JAMENDO_CLIENT_ID")
        url = "https://api.jamendo.com/v3.0/tracks/"
        
        params = {
            "client_id": client_id,
            "format": "json",
            "limit": limit,
            "fuzzytags": mood,
            "order": "popularity_total",
            "include": "musicinfo"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            tracks = []
            for item in data.get("results", []):
                tracks.append({
                    "id": item.get("id"),
                    "title": item.get("name"),
                    "artist": item.get("artist_name"),
                    "preview_url": item.get("audio"),
                    "album_image": item.get("image"),
                })
            return tracks
        except Exception as e:
            print(f"Jamendo Service Error: {e}")
            return []
