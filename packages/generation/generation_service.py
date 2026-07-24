import json

from packages.common.settings import settings
from packages.generation.context_formatter import ContextFormatter
from packages.generation.groq_client import GroqClient
from packages.generation.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

class AnswerGenerationService:
    def __init__(self):
        self.context_formatter = ContextFormatter()
        self.groq_client = GroqClient()
    
    def generate_answer(self, query: str, contexts: list[dict]) -> str:
        contexts = [self.context_formatter.enrich_context(ctx=ctx) for ctx in contexts]
        context_text = self.context_formatter.format_contexts(contexts=contexts)

        user_prompt = USER_PROMPT_TEMPLATE.format(
            context_text=context_text,
            query=query,
        )

        response = self.groq_client.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        if response.status_code != 200:
            print("Groq error status:", response.status_code)
            print("Groq error body:", response.text)
            response.raise_for_status()

        data = response.json()
        raw = data["choices"][0]["message"].get("content", "").strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            cleaned = raw.replace("```json", "").replace("```", "").strip()
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                return {"error": "JSON parse failed", "raw_output": raw}
            