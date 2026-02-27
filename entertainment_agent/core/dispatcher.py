from tools.gbooks_client import GBooksClient
from tools.itunespod_client import iTunesPodClient
from tools.lastfm_client import LastFMClient
from tools.tmdb_client import TMDBClient

import logging

logger = logging.getLogger("ToolDispatcher")

class ToolDispatcher:
    def __init__(self):
        self.tmdb = TMDBClient()
        self.lastfm = LastFMClient()
        self.gbooks = GBooksClient()
        self.itunespod = iTunesPodClient()

        self._dispatch_map = {
            "Movie": self._handle_tmdb,
            "TV Show": self._handle_tmdb,
            "Album": self._handle_lastfm,
            "Song": self._handle_lastfm,
            "Book": self._handle_gbooks,
            "Podcast": self._handle_itunespod,
            "Image": self._handle_itunespod_image
        }

    def _handle_tmdb(self, item):
        return self.tmdb.fetch_metadata(item["title"], item["media_type"])

    def _handle_lastfm(self, item):
        return self.lastfm.fetch_metadata(item["title"], item["media_type"])

    def _handle_gbooks(self, item):
        return self.gbooks.fetch_metadata(item["title"])

    def _handle_itunespod(self, item):
        return self.itunespod.fetch_metadata(item["title"])

    def _handle_itunespod_image(self, item):
        return self.itunespod.fetch_image(item["title"], item["media_type"])

    def _handle_placeholder(self, item):
        """Fallback handler for unknown media types."""
        logger.warning(f"No handler found for media type: {item.get('media_type')}")
        return None

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
            if not item['metadata'].get('image'):
                itunes_data = self._handle_itunespod_image(item['title'], media_type)
                if itunes_data:
                    item['metadata']['image'] = itunes_data.get('image')
            enriched_results.append(item)
            
        return enriched_results