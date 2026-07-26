from pathlib import Path
import json


INPUT_FILE = Path("data/chunks/fused/kev_nvd.chunks.jsonl")
OUTPUT_DIR = Path("data/metadata")


def main():
    vendors = set()
    products = set()

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)

            vendors.update(
                v.strip()
                for v in doc.get("vendor", [])
                if v and v.strip()
            )

            products.update(
                p.strip()
                for p in doc.get("product", [])
                if p and p.strip()
            )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with (OUTPUT_DIR / "vendors.json").open("w", encoding="utf-8") as f:
        json.dump(
            sorted(vendors),
            f,
            indent=2,
            ensure_ascii=False,
        )

    with (OUTPUT_DIR / "products.json").open("w", encoding="utf-8") as f:
        json.dump(
            sorted(products),
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"Vendors : {len(vendors)}")
    print(f"Products: {len(products)}")


if __name__ == "__main__":
    main()