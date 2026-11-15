
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
legacy_path = ROOT / "content" / "galerija.json"
entries_dir = ROOT / "content" / "galerija"
output_path = ROOT / "content" / "galerija-visi.json"

legacy = json.loads(legacy_path.read_text(encoding="utf-8"))
artworks = list(legacy.get("artworks", []))

seen = {a.get("id") for a in artworks}

for path in sorted(entries_dir.glob("*.json")):
    item = json.loads(path.read_text(encoding="utf-8"))

    if item.get("published") is False:
        continue

    identifier = "cms-" + path.stem

    if identifier in seen:
        continue

    artworks.append({
        "id": identifier,
        "title_lt": item.get("title", ""),
        "title_en": item.get("title_en") or item.get("title", ""),
        "details_lt": item.get("description", ""),
        "details_en": item.get("description_en") or item.get("description", ""),
        "image": item.get("image", ""),
        "category": item.get("period", "nauji"),
        "order": item.get("order", 100),
        "published": True,
    })

    seen.add(identifier)

def sort_order(item):
    try:
        return float(item.get("order") or 100)
    except (ValueError, TypeError):
        return 100

artworks.sort(key=sort_order)

output_path.write_text(
    json.dumps(
        {"artworks": artworks},
        ensure_ascii=False,
        indent=2
    ) + "\n",
    encoding="utf-8"
)

print(f"Generated {len(artworks)} artworks")
