import os
import json

from google import genai
from typing import Dict, Any
from dotenv import load_dotenv
import re
from datetime import datetime

load_dotenv()

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

def generate_emotion(user_emotion:str) -> Dict[str, Any]:
    system_prompt = f"""
    You are an expert emotion reflection tool.
    Your task is to analyze a user's input text and determine their dominant emotional state.

    Your response should include:
    - emotion: The primary emotion detected (e.g., "happiness", "sadness", "anger", "fear", "surprise", "neutral").
    - confidence: A float between 0.0 and 1.0 representing how confident the system is about the detected emotion.
    - analysis: A detailed explanation describing why this emotion was detected based on the input text.

    Return the result in the following JSON structure:
    {{
        "emotion": "emotion",
        "confidence": 0.5,
        "analysis": "analysis"
    }}

    Analyze this text: "{user_emotion}"
    """

    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=system_prompt
        )

        # Match the ```json ... ``` block
        match = re.search(r'```json\s*([\s\S]*?)\s*```', response.text, re.IGNORECASE)

        raw_json = None
        if match:
            raw_json = match.group(1).strip()
        else:
            raw_json = response_text.strip()



        emotions = json.loads(raw_json)

        emotions["created_at"] = datetime.utcnow()

        required_fields = ["emotion", "confidence", "analysis"]

        for field in required_fields:
            if field not in emotions:
                raise ValueError(f"Missing required field: {field}")

        return emotions

    except Exception as e:
        print("Error in generate_emotion:",e)
        return {
            "emotion": None,
            "confidence": None,
            "analysis": None,
            "created_at": datetime.utcnow(),
        }