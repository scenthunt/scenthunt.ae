#!/usr/bin/env python3
"""One-time import of the latest legacy CMS catalogue into the new per-fragrance collection.
Run after copying your CURRENT src/data/products.json into this upgraded project.
Will preserve new artwork and pricing fields unless they exist in the legacy record.
"""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
source = root / 'src/data/products.json'
dest = root / 'src/data/fragrances'
raw = json.loads(source.read_text())
assert isinstance(raw.get('products'), list), 'Legacy products.json needs a products array'
dest.mkdir(parents=True, exist_ok=True)
for item in raw['products']:
    slug = item['slug']
    if not slug or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in slug):
        raise ValueError(f'Unsafe fragrance slug: {slug!r}')
    path = dest / (slug + '.json')
    current = json.loads(path.read_text()) if path.exists() else {}
    current.update(item)  # newer CMS values win
    for size in (3, 5, 10):
        flag = f'offer{size}Ml'
        key = f'price{size}Ml'
        if flag not in item and (float(item.get(key) or 0) > 0 or int(item.get('sizeMl', 0)) == size):
            current[flag] = True
        elif flag not in current:
            current[flag] = False
        if key not in current or current[key] in (None, ''):
            current[key] = float(item.get('price') or 0) if int(item.get('sizeMl', 0)) == size else 0
    current.setdefault('artwork', '')
    current.setdefault('ingredientBackground', '')
    path.write_text(json.dumps(current, ensure_ascii=False, indent=2) + '\n')
    print('Synced', slug)
print('Finished. Check the individual files and commit them after review.')
