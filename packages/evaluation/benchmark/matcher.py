from __future__ import annotations

from datetime import datetime


def matches(doc: dict, filters: dict) -> bool:
    """
    Returns True if the document satisfies all filters.
    """

    for field, expected in filters.items():

        # --------------------------
        # Exact fields
        # --------------------------
        if field == "cve_id":
            if doc.get("cve_id") != expected:
                return False

        elif field == "vendor":
            if expected not in doc.get("vendor", []):
                return False

        elif field == "product":
            if expected not in doc.get("product", []):
                return False

        elif field == "cwe_id":
            if expected not in doc.get("cwe_ids", []):
                return False

        # --------------------------
        # Dates
        # --------------------------
        elif field == "published_year":
            published = doc.get("published_at")
            if not published or int(published[:4]) != expected:
                return False

        elif field == "published_after":
            published = doc.get("published_at")
            if not published:
                return False

            if datetime.fromisoformat(published) <= datetime.fromisoformat(expected):
                return False

        elif field == "due_date_before":
            due = doc.get("due_date")
            if not due:
                return False

            if datetime.fromisoformat(due) >= datetime.fromisoformat(expected):
                return False

        # --------------------------
        # String contains
        # --------------------------
        elif field == "required_action_contains":
            action = doc.get("required_action") or ""

            if expected.lower() not in action.lower():
                return False

        elif field == "known_ransomware_use":
            if doc.get("known_ransomware_use") != expected:
                return False

        # --------------------------
        # NVD metadata
        # --------------------------
        elif field == "severity":
            if doc.get("severity") != expected:
                return False

        elif field == "attack_vector":
            if doc.get("attack_vector") != expected:
                return False

        elif field == "attack_complexity":
            if doc.get("attack_complexity") != expected:
                return False

        elif field == "privileges_required":
            if doc.get("privileges_required") != expected:
                return False

        elif field == "cvss_score_gte":
            score = doc.get("cvss_score")

            if score is None or score < expected:
                return False

        else:
            raise ValueError(f"Unsupported filter: {field}")

    return True