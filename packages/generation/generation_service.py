import requests
import json
import re
from datetime import date

from packages.common.settings import settings
from packages.generation.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

class GenerationService:
    def __init__(self):
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

        self.api_key = settings.groq_api_key
        self.model = settings.groq_model
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
    
    def generate_answer(self, query: str, contexts: list[dict]) -> str:
        contexts = [self._enrich_context(ctx) for ctx in contexts]
        context_text = self._format_contexts(contexts)  # add this
                
        user_prompt = USER_PROMPT_TEMPLATE.format(
            context_text=context_text,
            query=query,
        )

        response = requests.post(
            self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.1,
            },
            timeout=60,
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
            
    def _format_contexts(self, contexts: list[dict]) -> str:
        parts = []
        for i, ctx in enumerate(contexts, start=1):
            fields = {
                "CVE ID": ctx.get("cve_id"),
                "Title": ctx.get("title"),
                "Vendor": ctx.get("vendor"),
                "Product": ctx.get("product"),
                "Patch Due Date": ctx.get("due_date") or self._extract_due_date(ctx.get("text", "")),
                "Patch Status": ctx.get("patch_status"),
                "Days Overdue": ctx.get("days_overdue"),
                "Known Ransomware Use": ctx.get("known_ransomware_use") or "not indicated in source",
                "Source": ctx.get("source_name"),
            }
            # only add NVD fields if they actually exist
            if ctx.get("cvss_score"):
                fields["CVSS Score"] = ctx.get("cvss_score")
            if ctx.get("severity"):
                fields["Severity"] = ctx.get("severity")
            if ctx.get("cwe_ids"):
                fields["CWE IDs"] = ctx.get("cwe_ids")
            if ctx.get("attack_vector"):
                fields["Attack Vector"] = ctx.get("attack_vector")
            if ctx.get("privileges_required"):
                fields["Privileges Required"] = ctx.get("privileges_required")

            lines = [f"[Source {i}]"]
            lines += [f"{k}: {v}" for k, v in fields.items()]
            lines.append(f"Evidence Text:\n{ctx.get('text', '')}")
            parts.append("\n".join(lines))

        return "\n\n".join(parts)
    

    def _enrich_context(self, ctx: dict) -> dict:
        # try structured field first
        due_raw = ctx.get("due_date") or ctx.get("Due Date")
        
        # fall back to parsing from raw text
        if not due_raw:
            text = ctx.get("text", "")
            match = re.search(r"Due Date:\s*(\d{4}-\d{2}-\d{2})", text)
            if match:
                due_raw = match.group(1)
        
        if not due_raw:
            ctx["patch_status"] = "INSUFFICIENT_DATA"
            ctx["days_overdue"] = 0
            return ctx
        
        try:
            due_date = date.fromisoformat(str(due_raw).strip())
            today = date.today()
            if due_date < today:
                ctx["patch_status"] = "OVERDUE"
                ctx["days_overdue"] = (today - due_date).days
            else:
                ctx["patch_status"] = "UPCOMING"
                ctx["days_overdue"] = 0
        except ValueError:
            ctx["patch_status"] = "INSUFFICIENT_DATA"
            ctx["days_overdue"] = 0
        
        return ctx
    
    def _extract_due_date(self, text: str) -> str | None:
        match = re.search(r"Due Date:\s*(\d{4}-\d{2}-\d{2})", text)
        return match.group(1) if match else None