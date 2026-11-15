import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
legacy_path = ROOT / 'content' / 'galerija.json'
entries_dir = ROOT / 'content' / 'galerija'
output_path = ROOT / 'content' / 'galerija-visi.json'

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sort_order(item):
    try:
        return float(item.get('order', 100))
    except (TypeError, ValueError, OverflowError):
        return 100.0

def main():
    cms_files = sorted(entries_dir.glob('*.json')) if entries_dir.exists() else []
    artworks = []
    if cms_files:
        for path in cms_files:
            item = read_json(path)
            if item.get('published') is False:
                continue
            artworks.append({
                'id': 'cms-' + path.stem,
                'title_lt': item.get('title', ''),
                'title_en': item.get('title_en') or item.get('title', ''),
                'details_lt': item.get('description', ''),
                'details_en': item.get('description_en') or item.get('description', ''),
                'image': item.get('image', ''),
                'category': item.get('period') or item.get('category') or 'nauji',
                'order': item.get('order', 100),
                'published': True,
            })
    elif legacy_path.exists():
        legacy = read_json(legacy_path)
        artworks = [item for item in legacy.get('artworks', []) if item.get('published') is not False]
    artworks.sort(key=sort_order)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({'artworks': artworks}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Generated {len(artworks)} artworks')

if __name__ == '__main__':
    main()
