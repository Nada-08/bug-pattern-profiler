import re


class CandidateGenerator:
    TOKEN_PATTERN = re.compile(r"[A-Za-z0-9.+#-]+")

    def __init__(self, max_ngram: int = 3):
        self.max_ngram = max_ngram

    def generate(self, query: str) -> list[str]:
        tokens = self.TOKEN_PATTERN.findall(query.strip())

        candidates = []
        seen = set()

        for n in range(min(self.max_ngram, len(tokens)), 0, -1):
            for i in range(len(tokens) - n + 1):
                phrase = " ".join(tokens[i:i + n])

                if phrase not in seen:
                    seen.add(phrase)
                    candidates.append(phrase)

        return candidates