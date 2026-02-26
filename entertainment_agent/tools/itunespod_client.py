import logging
import requests

logger = logging.getLogger("PodcastTool")

class iTunesPodClient:
    def __init__(self):
        # No API Key required for iTunes Search!
        self.base_url = "https://itunes.apple.com/search"

    def fetch_metadata(self, title):
        """
        Searches iTunes for a podcast title and returns the top match.
        """
        params = {
            "term": title,
            "media": "podcast",
            "limit": 1
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = data.get("results", [])
            if not results:
                logger.info(f"No podcast found for title: {title}")
                return None

            podcast = results[0]
            
            return {
                "official_title": podcast.get("collectionName"),
                "artist": podcast.get("artistName"),
                "genres": podcast.get("genres", []),
                "feed_url": podcast.get("feedUrl"),
                "itunes_url": podcast.get("collectionViewUrl"),
                "artwork": podcast.get("artworkUrl600")
            }
        except Exception as e:
            logger.error(f"iTunes Podcast search failed for {title}: {e}")
            return None