import logging
import os
import requests

logger = logging.getLogger("BooksTool")

class BooksClient:
    def __init__(self):
        self.api_key = os.getenv("GBOOKS_API_KEY")
        self.base_url = "https://www.googleapis.com/books/v1/volumes"

    def fetch_metadata(self, title):
        """
        Searches Google Books for a title and returns the top match.
        """
        params = {
            "q": f"intitle:{title}",
            "maxResults": 1,
            "key": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            items = data.get("items", [])
            if not items:
                logger.info(f"No book found for title: {title}")
                return None

            volume_info = items[0].get("volumeInfo", {})
            
            return {
                "official_title": volume_info.get("title"),
                "authors": volume_info.get("authors", []),
                "description": volume_info.get("description", "No description available."),
                "page_count": volume_info.get("pageCount"),
                "categories": volume_info.get("categories", []),
                "preview_link": volume_info.get("previewLink")
            }
        except Exception as e:
            logger.error(f"Google Books search failed for {title}: {e}")
            return None