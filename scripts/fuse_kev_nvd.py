from pathlib import Path

from packages.ingestion.fusion.kev_nvd_fuser import fuse_kev_with_nvd

fuse_kev_with_nvd(
    kev_path=Path("data/normalized/cisa_kev/cisa_kev.normalized.jsonl"),
    nvd_path=Path("data/normalized/nvd/nvd_page_0.normalized.jsonl"),
    output_path=Path("data/normalized/fused/kev_nvd.normalized.jsonl"),
)