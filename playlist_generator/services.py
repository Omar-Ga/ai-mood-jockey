import os
import requests
from dotenv import load_dotenv

load_dotenv()

class JamendoService:
    @staticmethod
    def _fetch(params):
        """Internal helper to call the Jamendo tracks endpoint."""
        client_id = os.getenv("JAMENDO_CLIENT_ID")
        url = "https://api.jamendo.com/v3.0/tracks/"
        base = {
            "client_id": client_id,
            "format": "json",
            "include": "musicinfo",
        }
        base.update(params)
        try:
            response = requests.get(url, params=base, timeout=10)
            response.raise_for_status()
            results = response.json().get("results", [])
            return [
                {
                    "id": item.get("id"),
                    "title": item.get("name"),
                    "artist": item.get("artist_name"),
                    "preview_url": item.get("audio"),
                    "album_image": item.get("image"),
                }
                for item in results
            ]
        except Exception as e:
            print(f"Jamendo Service Error: {e}")
            return []

    @staticmethod
    def get_tracks(genres, moods, keywords, limit=24):
        """
        Tiered search strategy:
        1. Highly specific: Genre + Mood combination
        2. Specific: Mood + Keyword combination
        3. Mood only (often most important for feeling-based queries)
        4. Genre only
        5. Keyword only (fuzzy)
        """
        tracks = []
        seen_ids = set()

        def add_tracks(new_tracks):
            for t in new_tracks:
                if t["id"] not in seen_ids:
                    seen_ids.add(t["id"])
                    tracks.append(t)

        safe_genres = [g.lower() for g in genres] if genres else []
        safe_moods = [m.lower() for m in moods] if moods else []
        safe_keywords = [k.lower() for k in keywords] if keywords else []

        # --- Pass 1: Genre + Mood Combo (Highest Relevance) ---
        if len(tracks) < limit and safe_genres and safe_moods:
            tag_combo = f"{safe_genres[0]}+{safe_moods[0]}"
            results = JamendoService._fetch({
                "tags": tag_combo,
                "limit": limit - len(tracks),
                "order": "popularity_week",
            })
            add_tracks(results)

        # --- Pass 2: Mood + Keyword Combo ---
        if len(tracks) < limit and safe_moods and safe_keywords:
            tag_combo = f"{safe_moods[0]}+{safe_keywords[0]}"
            results = JamendoService._fetch({
                "fuzzytags": tag_combo,
                "limit": limit - len(tracks),
                "order": "popularity_month",
            })
            add_tracks(results)

        # --- Pass 3: Mood only (Mood drives the vibe more than genre) ---
        if len(tracks) < limit and safe_moods:
            results = JamendoService._fetch({
                "tags": safe_moods[0],
                "limit": limit - len(tracks),
                "order": "popularity_week",
                "boost": "popularity_month"
            })
            add_tracks(results)

        # --- Pass 4: Primary genre fallback ---
        if len(tracks) < limit and safe_genres:
            results = JamendoService._fetch({
                "tags": safe_genres[0],
                "limit": limit - len(tracks),
                "order": "popularity_week",
            })
            add_tracks(results)
            
        # --- Pass 5: Keyword fallback (fuzzy search) ---
        if len(tracks) < limit and safe_keywords:
            results = JamendoService._fetch({
                "fuzzytags": safe_keywords[0],
                "limit": limit - len(tracks),
                "order": "popularity_total",
            })
            add_tracks(results)

        # --- Ultimate fallback: generic popular tracks ---
        if not tracks:
            results = JamendoService._fetch({
                "tags": "pop",
                "limit": limit,
                "order": "popularity_total",
            })
            add_tracks(results)

        return tracks[:limit]
