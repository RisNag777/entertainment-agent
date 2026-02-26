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

    def _ensure_file_exists(self):
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, 'w') as f:
                json.dump({"taste_profile": {"core_themes": []}}, f)

    def load(self):
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def merge_and_save(self, brain_update):
        current_memory = self.load()
        
        # Merge themes while avoiding duplicates
        new_themes = brain_update.get("memory_update", {}).get("add_themes", [])
        updated_themes = list(set(current_memory["taste_profile"]["core_themes"] + new_themes))
        
        current_memory["taste_profile"]["core_themes"] = updated_themes
        
        with open(self.filepath, 'w') as f:
            json.dump(current_memory, f, indent=4)
        
        logger.info(f"Memory updated with {len(new_themes)} new themes.")
        return current_memory