from dotenv import load_dotenv
from openai import OpenAI

from core.dispatcher import ToolDispatcher
from core.memory import MemoryManager
from core.schemas import oracle_schema

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