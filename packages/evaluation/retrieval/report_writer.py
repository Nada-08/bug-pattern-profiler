from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from packages.evaluation.retrieval.results import EvaluationResult

REPORTS_DIR = Path("reports/retrieval")

class ReportWriter:

    def __init__(self):
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    def write(self, result: EvaluationResult) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        output = REPORTS_DIR / f"retrieval_{result.namespace}_{timestamp}.json"

        with output.open("w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2)

        latest = REPORTS_DIR / f"retrieval_{result.namespace}_latest.json"

        with latest.open("w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2)

        return output