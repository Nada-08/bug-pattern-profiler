import re
from datetime import date


class ContextFormatter:
    @staticmethod
    def format_contexts(contexts: list[dict]) -> str:
        parts = []
        for i, ctx in enumerate(contexts, start=1):
            fields = {
                "CVE ID": ctx.cve_id,
                "Title": ctx.title,
                "Vendor": ctx.vendor,
                "Product": ctx.product,
                "Patch Due Date": ctx.due_date or ContextFormatter._extract_due_date(ctx.text),
                "Patch Status": ctx.patch_status,
                "Days Overdue": ctx.days_overdue,
                "Known Ransomware Use": ctx.known_ransomware_use or "not indicated in source",
                "Source": ctx.source_name,
            }
            # only add NVD fields if they actually exist
            if ctx.cvss_score:
                fields["CVSS Score"] = ctx.cvss_score
            if ctx.severity:
                fields["Severity"] = ctx.severity
            if ctx.cwe_ids:
                fields["CWE IDs"] = ctx.cwe_ids
            if ctx.attack_vector:
                fields["Attack Vector"] = ctx.attack_vector
            if ctx.privileges_required:
                fields["Privileges Required"] = ctx.privileges_required

            lines = [f"[Source {i}]"]
            lines += [f"{k}: {v}" for k, v in fields.items()]
            lines.append(f"Evidence Text:\n{ctx.text or ''}")
            parts.append("\n".join(lines))

        return "\n\n".join(parts)
    
    @staticmethod    
    def enrich_context(ctx: dict) -> dict:
        # try structured field first
        due_raw = ctx.due_date
        
        # fall back to parsing from raw text
        if not due_raw:
            text = ctx.text
            match = re.search(r"Due Date:\s*(\d{4}-\d{2}-\d{2})", text)
            if match:
                due_raw = match.group(1)
        
        if not due_raw:
            ctx.patch_status = "INSUFFICIENT_DATA"
            ctx.days_overdue = 0
            return ctx
        
        try:
            due_date = date.fromisoformat(str(due_raw).strip())
            today = date.today()
            if due_date < today:
                ctx.patch_status = "OVERDUE"
                ctx.days_overdue = (today - due_date).days
            else:
                ctx.patch_status = "UPCOMING"
                ctx.days_overdue = 0
        except ValueError:
            ctx.patch_status = "INSUFFICIENT_DATA"
            ctx.days_overdue = 0
        
        return ctx
    
    @staticmethod
    def _extract_due_date(text: str) -> str | None:
        match = re.search(r"Due Date:\s*(\d{4}-\d{2}-\d{2})", text)
        return match.group(1) if match else None