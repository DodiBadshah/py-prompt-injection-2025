"""
Payload catalog loader for py-prompt-injection-2025.
Loads and validates all YAML payload files from the catalog directory.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel

from llm_probe_2025.schemas import Payload


CATALOG_DIR = Path(__file__).parent / "catalog"


class PayloadCatalog(BaseModel):
    category: str
    name: str
    description: str
    source: str
    payloads: list[Payload]


def load_catalog(catalog_path: Path) -> PayloadCatalog:
    with open(catalog_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    catalog = PayloadCatalog(**data)
    for p in catalog.payloads:
        p.category = catalog.category
    return catalog


def load_all_catalogs(
    category_filter: str | None = None,
) -> list[Payload]:
    """
    Load all payload catalogs from the catalog directory.
    Optionally filter by OWASP category prefix (e.g. 'LLM01').
    Returns a flat list of Payload objects with category tagged.
    """
    all_payloads: list[Payload] = []

    for yaml_file in sorted(CATALOG_DIR.glob("*.yaml")):
        catalog = load_catalog(yaml_file)
        if category_filter:
            if not catalog.category.startswith(category_filter):
                continue
        all_payloads.extend(catalog.payloads)

    return all_payloads


def get_catalog_summary() -> dict[str, Any]:
    """
    Return a summary of all loaded catalogs: category, name, payload count.
    """
    summary = {}
    for yaml_file in sorted(CATALOG_DIR.glob("*.yaml")):
        catalog = load_catalog(yaml_file)
        summary[catalog.category] = {
            "name": catalog.name,
            "payload_count": len(catalog.payloads),
            "payload_ids": [p.id for p in catalog.payloads],
        }
    return summary


if __name__ == "__main__":
    summary = get_catalog_summary()
    total = 0
    for category, info in summary.items():
        print(f"{category}: {info['name']} - {info['payload_count']} payloads")
        total += info["payload_count"]
    print(f"\nTotal payloads: {total}")
