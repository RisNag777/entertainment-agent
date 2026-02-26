from dotenv import load_dotenv
from openai import OpenAI

from core.dispatcher import ToolDispatcher
from core.memory import MemoryManager

import json
import logging
import os

load_dotenv()
prompt_path = os.getenv("ENTERTAINMENT_PROMPT_PATH")

# Setting up a basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("EntertainmentOracle")

oracle_schema = {
    "name": "update_entertainment_profile",
    "description": "Analyzes a user like and updates the taste graph memory with a 6-item multimedia grid.",
    "parameters": {
        "type": "object",
        "properties": {
            "analysis": {
                "type": "string", 
                "description": "Technical breakdown of the user's latest 'Like' and how it maps to their profile."
            },
            "extracted_traits": {
                "type": "array", 
                "items": {"type": "string"},
                "description": "Key mood, style, or thematic elements identified in the input."
            },
            "memory_update": {
                "type": "object",
                "properties": {
                    "add_themes": {"type": "array", "items": {"type": "string"}},
                    "weight_adjustments": {
                        "type": "object", 
                        "additionalProperties": {"type": "number"}
                    }
                },
                "required": ["add_themes", "weight_adjustments"]
            },
            "taste_grid": {
                "type": "array",
                "description": "A curated 6-item list providing exactly one recommendation for each media type.",
                "items": {
                    "type": "object",
                    "properties": {
                        "media_type": {
                            "type": "string", 
                            "enum": ["Movie", "TV Show", "Album", "Song", "Podcast", "Book"]
                        },
                        "title": {"type": "string"},
                        "reasoning": {"type": "string", "description": "Explicitly link this recommendation to the extracted_traits."}
                    },
                    "required": ["media_type", "title", "reasoning"]
                },
                "minItems": 6,
                "maxItems": 6
            }
        },
        "required": ["analysis", "extracted_traits", "memory_update", "taste_grid"]
    }
}

class EntertainmentBrain:
    def __init__(self, model = "gpt-4o-mini"):
        self.model = model
        with open(prompt_path, 'r') as f:
            self.system_prompt = f.read()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        logger.info(f"Brain initialized with model: {self.model}")
        self.memory = MemoryManager()

    def get_recommendation(self, user_input):
        logger.info(f"Processing user input...")
        current_memory = self.memory.load()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Memory: {json.dumps(current_memory)}\nInput: {user_input}"}
                ],
                tools=[{"type": "function", "function": oracle_schema}],
                tool_choice={"type": "function", "function": {"name": "update_entertainment_profile"}}
            )
            tool_call = response.choices[0].message.tool_calls[0]
            raw_result = json.loads(tool_call.function.arguments)
            dispatcher = ToolDispatcher()
            enriched_grid = dispatcher.enrich_grid(raw_result["taste_grid"])
            raw_result["taste_grid"] = enriched_grid
            self.memory.merge_and_save(raw_result)
            logger.info("Successfully generated recommendation and memory update.")
            return raw_result
        except Exception as e:
            logger.error(f"Failed to get recommendation: {e}")
            raise