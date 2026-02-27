from dotenv import load_dotenv

import json
import logging
import os

load_dotenv()
memory_filepath = os.getenv("MEMORY_FILEPATH", "data/memory.json")

logger = logging.getLogger("EntertainmentOracle")

class MemoryManager:
    def __init__(self):
        self.filepath = memory_filepath
        self._ensure_file_exists()
        self.current_memory = self.load()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, 'w') as f:
                json.dump({"taste_profile": {"core_themes": [], "theme_weights": {}}}, f)

    def load(self):
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def merge_and_save(self, brain_update):        
        # Initialize taste_profile structure if it doesn't exist
        if "taste_profile" not in self.current_memory:
            self.current_memory["taste_profile"] = {"core_themes": [], "theme_weights": {}}
        
        # Merge themes while avoiding duplicates
        new_themes = brain_update.get("memory_update", {}).get("add_themes", [])
        updated_themes = list(set(self.current_memory["taste_profile"]["core_themes"] + new_themes))
        self.current_memory["taste_profile"]["core_themes"] = updated_themes
        
        # Merge weight adjustments
        weight_adjustments = brain_update.get("memory_update", {}).get("weight_adjustments", {})
        if "theme_weights" not in self.current_memory["taste_profile"]:
            self.current_memory["taste_profile"]["theme_weights"] = {}
        
        for theme, adjustment in weight_adjustments.items():
            current_weight = self.current_memory["taste_profile"]["theme_weights"].get(theme, 0.0)
            self.current_memory["taste_profile"]["theme_weights"][theme] = current_weight + adjustment
        
        with open(self.filepath, 'w') as f:
            json.dump(self.current_memory, f, indent=4)
        
        logger.info(f"Memory updated with {len(new_themes)} new themes.")
        return self.current_memory
    
    def get_weights(self):
        """
        Get the current theme weights from memory.
        
        Returns:
            dict: Dictionary mapping theme names to their weights, or None if no weights exist
        """
        weights = self.current_memory.get("taste_profile", {}).get("theme_weights", {})
        return weights if weights else None