"""Schema definitions for the entertainment agent."""

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
