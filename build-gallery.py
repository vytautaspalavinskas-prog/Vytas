import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
legacy_path = ROOT / 'content' / 'galerija.json'
entries_dir = ROOT / 'content' / 'galerija'
output_path = ROOT / 'content' / 'galerija-visi.json'


def read_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8-sig'))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f'Cannot read valid JSON from {path}: {exc}') from exc


def sort_order(item):
    value = item.get('order', 100)
    try:
        return float(value) if value is not None and str(value).strip() else 100.0
    except (TypeError, ValueError, OverflowError):
        return 100.0


def main():
    legacy = read_json(legacy_path) if legacy_path.exists() else {'artworks': []}
    legacy_artworks = legacy.get('artworks', [])
    if not isinstance(legacy_artworks, list):
        raise ValueError('Legacy gallery artworks must be a list')

    cms_files = sorted(entries_dir.glob('*.json'))
    cms_stems = {path.stem for path in cms_files}
    legacy_by_id = {item.get('id'): item for item in legacy_artworks if isinstance(item, dict)}

    # Keep legacy entries only until a matching CMS file exists.
    artworks = [item.copy() for item in legacy_artworks
                if isinstance(item, dict) and item.get('id') not in cms_stems]
    seen = {item.get('id') for item in artworks}

    for path in cms_files:
        item = read_json(path)
        if not isinstance(item, dict):
            raise ValueError(f'CMS entry must be a JSON object: {path}')
        if item.get('published') is False:
            continue

        identifier = 'cms-' + path.stem
        if identifier in seen:
            continue

        previous = legacy_by_id.get(path.stem, {})
        artworks.append({
            'id': identifier,
            'title_lt': item.get('title', ''),
            'title_en': item.get('title_en') or item.get('title', ''),
            'details_lt': item.get('description', ''),
            'details_en': item.get('description_en') or item.get('description', ''),
            'image': item.get('image', ''),
            'category': item.get('period') or previous.get('category', 'nauji'),
            'order': item.get('order', 100),
            'published': True,
        })
        seen.add(identifier)

    # Python's stable sort preserves original order for equal values.
    artworks.sort(key=sort_order)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps({'artworks': artworks}, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    print(f'Generated {len(artworks)} artworks')


if __name__ == '__main__':
    main()
