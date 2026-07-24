import requests

from packages.common.settings import settings

class GroqClient:
    def __init__(self):
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

        self.api_key = settings.groq_api_key
        self.model = settings.groq_model
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    def generate(
        self,
        system_prompt: str, 
        user_prompt: str
    ) -> dict:
        return requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.1,
                },
                timeout=60,
            )

        