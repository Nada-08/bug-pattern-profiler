from pathlib import Path

from rapidfuzz import fuzz, process

from packages.retrieval.models import VendorProductMatch
from packages.ingestion.storage.local_store import load_values


class VendorProductResolver:
    def __init__(
        self,
        vendors: list[str] | None = None,
        products: list[str] | None = None,
        threshold: int = 85,
    ):
        metadata_dir = Path(__file__).resolve().parents[3] / "data" / "metadata"

        self.vendors = vendors or load_values(metadata_dir / "vendors.txt")
        self.products = products or load_values(metadata_dir / "products.txt")
        self.threshold = threshold


    def extract(self, candidates: list[str]) -> VendorProductMatch:
        vendor, vendor_score = self._resolve(candidates, self.vendors)
        product, product_score = self._resolve(candidates, self.products)

        return VendorProductMatch(
            vendor=vendor,
            vendor_confidence=vendor_score,
            product=product,
            product_confidence=product_score,
        )
    
    def _resolve(
        self,
        candidates: list[str],
        choices: list[str],
    ) -> tuple[str | None, float]:

        if not choices:
            return None, 0.0

        best_value = None
        best_score = 0.0

        for candidate in candidates:
            match = process.extractOne(
                candidate,
                choices,
                scorer=fuzz.WRatio,
            )

            if match is None:
                continue

            value, score, _ = match

            if score > best_score:
                best_score = score
                best_value = value

        if best_score < self.threshold:
            return None, best_score

        return best_value, best_score