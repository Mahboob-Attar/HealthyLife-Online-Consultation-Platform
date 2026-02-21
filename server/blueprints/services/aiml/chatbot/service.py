import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("OPENROUTER_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


class ChatbotService:

    @staticmethod
    def respond(data):

        user_msg = data.get("message", "").strip()

        if not user_msg:
            return "Please enter a message."

        try:
            payload = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpful virtual nurse. Provide safe medical guidance."},
                    {"role": "user", "content": user_msg}
                ]
            }

            response = requests.post(API_URL, headers=headers, json=payload)

            result = response.json()

            return result["choices"][0]["message"]["content"]

        except Exception as e:
            import traceback
            traceback.print_exc()
            return "AI service unavailable."