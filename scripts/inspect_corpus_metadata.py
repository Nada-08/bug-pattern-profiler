from pathlib import Path
import json

from packages.evaluation.analysis.metadata_profiler import MetadataProfiler


INPUT_FILE = Path("data/chunks/fused/kev_nvd.chunks.jsonl")
OUTPUT_DIR = Path("packages/evaluation")
OUTPUT_FILE = OUTPUT_DIR / "metadata_profile.json"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    profiler = MetadataProfiler(INPUT_FILE)
    report = profiler.profile()

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Analysis complete!")
    print(f"Input : {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()