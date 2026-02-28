import os
import json
from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class MoodAnalysisSchema(BaseModel):
    genres: list[str] = Field(description="1-2 relevant music genres")
    moods: list[str] = Field(description="1-2 relevant music moods")
    keywords: list[str] = Field(description="1-2 relevant music keywords")

class GeminiService:
    @staticmethod
    def analyze_mood(user_input):
        """
        Takes user's natural language input and translates it to music parameters.
        Returns a dict: {"error": "..."} or {"genres": [...], "moods": [...], "keywords": [...]}
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {"error": "GEMINI_API_KEY not found in environment variables."}

        # Use the modern GenAI Client
        client = genai.Client(api_key=api_key)
        
        # Use the latest flash model for speed and capability
        model_id = "gemini-3-flash-preview"

        prompt = f"""
        Act as a professional music curator and semantic translator. Your task is to analyze the user's natural language text (which may describe feelings, weather, activities, or vague scenarios) and translate it into precise musical parameters: genres, moods, and keywords.
        
        CRITICAL: To ensure valid database lookups, prioritize these standard Jamendo-compatible tags where possible:
        - Allowed Genres: pop, rock, electronic, hiphop, jazz, indie, classical, ambient, chillout, metal, acoustic, rnb
        - Allowed Moods: happy, sad, chill, energetic, relax, dark, romantic, uplifting, calm, heavy, focus, melancholic
        
        Guidelines:
        - Extract 1-2 relevant standard music genres.
        - Extract 1-2 descriptive mood adjectives.
        - Extract 1-2 thematic keywords related to the activity or setting (e.g., "study", "rain", "workout", "party", "sleep").
        
        Examples:
        User Text: "I'm stressed about finals and need to focus"
        Output: {{"genres": ["chillout", "ambient"], "moods": ["focus", "calm"], "keywords": ["study", "concentration"]}}
        
        User Text: "Hitting the gym hard today, need something aggressive"
        Output: {{"genres": ["metal", "electronic"], "moods": ["energetic", "heavy"], "keywords": ["workout", "gym"]}}
        
        User Text: "Sitting by the window watching the rain"
        Output: {{"genres": ["jazz", "acoustic"], "moods": ["melancholic", "chill"], "keywords": ["rain", "cozy"]}}

        User Text: "{user_input}"
        """

        try:
            # Generate content with structured response schema (Pydantic)
            # This ensures valid JSON matching our schema without brittle string parsing
            response = client.models.generate_content(
                model=model_id,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": MoodAnalysisSchema,
                }
            )
            
            # The SDK automatically parses the JSON into our Pydantic model
            if response.parsed:
                return response.parsed.model_dump()
            
            # Fallback if parsing fails but text exists (extremely unlikely with structured output)
            return json.loads(response.text)
            
        except Exception as e:
            print(f"Gemini Service Error: {e}")
            return {"error": "Failed to analyze mood using AI."}
