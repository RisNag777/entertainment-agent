import logging
import os
import requests

logger = logging.getLogger("LastFMTool")

class LastFMClient:
    def __init__(self):
        self.api_key = os.getenv("LASTFM_API_KEY")
        self.base_url = "http://ws.audioscrobbler.com/2.0/"

    def fetch_metadata(self, title, media_type):
        """
        Routes the request to either album or track search based on media_type.
        """
        if media_type == "Album":
            return self._search_album(title)
        elif media_type == "Song":
            return self._search_track(title)
        return None

    def _search_album(self, album_name):
        params = {
            "method": "album.search",
            "album": album_name,
            "api_key": self.api_key,
            "format": "json",
            "limit": 1
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            results = response.json().get("results", {}).get("albummatches", {}).get("album", [])
            
            if results:
                album = results[0]
                return {
                    "official_title": album.get("name"),
                    "artist": album.get("artist"),
                    "url": album.get("url"),
                    "image": album.get("image")[-1].get("#text") # Gets the largest image
                }
        except Exception as e:
            logger.error(f"Last.fm Album search failed: {e}")
        return None

    def _search_track(self, track_name):
        params = {
            "method": "track.search",
            "track": track_name,
            "api_key": self.api_key,
            "format": "json",
            "limit": 1
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            results = response.json().get("results", {}).get("trackmatches", {}).get("track", [])
            
            if results:
                track = results[0]
                return {
                    "official_title": track.get("name"),
                    "artist": track.get("artist"),
                    "url": track.get("url"),
                    "listeners": track.get("listeners")
                }
        except Exception as e:
            logger.error(f"Last.fm Track search failed: {e}")
        return None