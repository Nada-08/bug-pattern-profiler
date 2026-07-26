import re


class RegexExtractor:
    CVE_PATTERN = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)
    CWE_PATTERN = re.compile(r"CWE-\d+", re.IGNORECASE)
    YEAR_PATTERN = re.compile(r"\b20\d{2}\b")

    def extract(self, query: str) -> dict:
        return {
            "cve_id": self._extract_cve(query),
            "cwe_ids": self._extract_cwe(query),
            "published_year": self._extract_year(query),
        }

    def _extract_cve(self, query: str) -> str | None:
        match = self.CVE_PATTERN.search(query)
        return match.group(0).upper() if match else None

    def _extract_cwe(self, query: str) -> list[str] | None:
        matches = self.CWE_PATTERN.findall(query)
        return [m.upper() for m in matches] or None

    def _extract_year(self, query: str) -> int | None:
        # Don't mistake the year inside a CVE ID
        query = self.CVE_PATTERN.sub("", query)

        match = self.YEAR_PATTERN.search(query)
        return int(match.group()) if match else None