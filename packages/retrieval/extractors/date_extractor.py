from datetime import datetime
import re


class DateExtractor:
    CURRENT_YEAR = datetime.now().year

    YEAR_PATTERNS = [
        r"(?:published|from|during|in)\s+(20\d{2})",
        r"\b(20\d{2})\b",  # fallback
    ]

    def extract(self, query: str) -> dict:
        return {
            "published_year": self._extract_published_year(query),
        }

    def _extract_published_year(self, query: str) -> int | None:
        query = query.lower()

        if "this year" in query:
            return self.CURRENT_YEAR

        if "last year" in query:
            return self.CURRENT_YEAR - 1

        for pattern in self.YEAR_PATTERNS:
            match = re.search(pattern, query)

            if match:
                return int(match.group(1))

        return None