import os
import requests
from django.conf import settings

class JamendoService:
    @staticmethod
    def get_tracks_by_mood(mood, limit=10):
        client_id = os.getenv("JAMENDO_CLIENT_ID")
        url = "https://api.jamendo.com/v3.0/tracks/"
        
        params = {
            "client_id": client_id,
            "format": "json",
            "limit": limit,
            "fuzzytags": mood,
            "order": "popularity_total",
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                results = response.json().get("results", [])
                return [
                    {
                        "id": track["id"],
                        "title": track["name"],
                        "artist": track["artist_name"],
                        "preview": track["audio"]
                    }
                    for track in results
                ]
            return []
        except Exception as e:
            print(f"Jamendo Service Error: {e}")
            return []
