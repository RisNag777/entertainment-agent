import logging
import os
import requests

logger = logging.getLogger("TMDBTool")

class TMDBClient:
    def __init__(self):
        self.access_token = os.getenv("TMDB_ACCESS_KEY")
        self.base_url = "https://api.themoviedb.org/3"

    @property
    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json;charset=utf-8"
        }

    def fetch_metadata(self, title, media_type):
        """
        Searches for a title and returns the most relevant match.
        """
        search_type = "movie" if media_type == "Movie" else "tv"
        url = f"{self.base_url}/search/{search_type}"
        params = {"query": title}
        
        try:
            response = requests.get(url, headers=self._headers, params=params)
            response.raise_for_status()
            results = response.json().get("results", [])
            
            if not results:
                logger.info(f"No results found for {title}")
                return None

            top_match = results[0]
            return {
                "official_title": top_match.get("title") or top_match.get("name"),
                "overview": top_match.get("overview"),
                "release_date": top_match.get("release_date") or top_match.get("first_air_date"),
                "tmdb_id": top_match.get("id"),
                "popularity": top_match.get("popularity")
            }
        except Exception as e:
            logger.error(f"TMDB search failed for {title}: {e}")
            return None
    
    def get_recommendations(self, tmdb_id, media_type="Movie"):
        """
        Fetches a list of recommended movies or TV shows based on a specific ID.
        """
        category = "movie" if media_type == "Movie" else "tv"
        url = f"{self.base_url}/{category}/{tmdb_id}/recommendations"
        
        try:
            response = requests.get(url, headers=self._headers)
            response.raise_for_status()
            results = response.json().get("results", [])
            
            # Return top 3 recommendations for the brain to consider
            return [{
                "title": r.get("title") or r.get("name"),
                "overview": r.get("overview"),
                "release_date": r.get("release_date") or r.get("first_air_date")
            } for r in results[:3]]
        except Exception as e:
            logger.error(f"Failed to fetch recommendations for ID {tmdb_id}: {e}")
            return []