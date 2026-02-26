from tools.lastfm_client import LastFMClient
from tools.tmdb_client import TMDBClient

import logging

logger = logging.getLogger("ToolDispatcher")

class ToolDispatcher:
    def __init__(self):
        self.tmdb = TMDBClient()
        self.lastfm = LastFMClient()

        self._dispatch_map = {
            "Movie": self._handle_tmdb,
            "TV Show": self._handle_tmdb,
            "Album": self._handle_lastfm,
            "Song": self._handle_lastfm,
            "Book": self._handle_placeholder,
            "Podcast": self._handle_placeholder
        }

    def _handle_tmdb(self, item):
        return self.tmdb.fetch_metadata(item["title"], item["media_type"])

    def _handle_lastfm(self, item):
        return self.lastfm.fetch_metadata(item["title"], item["media_type"])

    def _handle_placeholder(self, item):
        logger.warning(f"No API tool currently implemented for {item['media_type']}")
        return {"status": "provider_not_implemented"}

    def enrich_grid(self, taste_grid):
        """
        Iterates through the 6-item grid and fetches real metadata for each.
        """
        enriched_results = []
        for item in taste_grid:
            media_type = item.get("media_type")
            handler = self._dispatch_map.get(media_type, self._handle_placeholder)
            
            logger.info(f"Enriching {media_type}: {item['title']}")
            metadata = handler(item)
            
            # Attach the real data to the recommendation
            item["metadata"] = metadata
            enriched_results.append(item)
            
        return enriched_results