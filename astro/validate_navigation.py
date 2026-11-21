#!/usr/bin/env python3
"""Check Astro navigation integrity against the fork's Shopify category source."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAV = ROOT / "astro" / "automotive-navigation.json"
SOURCE = ROOT / "data" / "categories" / "vp_vehicles_parts.yml"

def read_shopify_categories():
    data = {}
    current = None
    for line in SOURCE.read_text(encoding="utf-8").splitlines():
        if line.startswith("- id: vp"):
            current = line.removeprefix("- id: ").strip()
        elif current is not None and line.startswith("  name: "):
            data[current] = line.removeprefix("  name: ")
            current = None
    return data

def main():
    nav = json.loads(NAV.read_text(encoding="utf-8"))
    source = read_shopify_categories()
    assert nav["schema_version"] == 1 and nav["lifecycle"] == "draft_review_required"
    assert nav["fallback"]["source_id"] in source
    seen = set()
    parts = 0
    groups = 0
    for section in nav["sections"]:
        assert section["id"].startswith("astro:section/") and section["groups"]
        for group in section["groups"]:
            assert group["id"].startswith("astro:group/") and group["parts"]
            groups += 1
            for part in group["parts"]:
                parts += 1
                assert part["id"] not in seen, part["id"]
                seen.add(part["id"])
                if part["source"] == "shopify":
                    assert part["id"] == "shopify:" + part["source_id"]
                    assert source.get(part["source_id"]) == part["label"], part
                else:
                    assert part["source"] == "astro" and part["status"] == "proposed"
                    assert part["id"].startswith("astro:part/")
    print("PASS: %d sections, %d groups, %d part types validated" % (len(nav["sections"]), groups, parts))

if __name__ == "__main__":
    main()
