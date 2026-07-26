import re


class QueryNormalizer:
    def normalize(self, query: str) -> str:
        query = self._normalize_whitespace(query)
        query = self._normalize_cve(query)
        query = self._normalize_cwe(query)
        return query

    def _normalize_whitespace(self, query: str) -> str:
        return " ".join(query.split())

    def _normalize_cve(self, query: str) -> str:
        """
        Converts common CVE variants into:
        CVE-YYYY-NNNN

        Examples:
            cve20251234
            CVE20251234
            cve 2025 1234
            cve_2025_1234
            cve-2025_1234
        """

        pattern = re.compile(
            r"(?i)cve[\s\-_]*(20\d{2})[\s\-_]*(\d{4,7})"
        )

        return pattern.sub(
            lambda m: f"CVE-{m.group(1)}-{m.group(2)}",
            query,
        )

    def _normalize_cwe(self, query: str) -> str:
        """
        Converts common CWE variants into:
        CWE-79
        """

        pattern = re.compile(
            r"(?i)cwe[\s\-_]*(\d+)"
        )

        return pattern.sub(
            lambda m: f"CWE-{m.group(1)}",
            query,
        )