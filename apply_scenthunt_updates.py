#!/usr/bin/env python3
"""Apply narrow ScentHunt UI and policy updates to the original Astro structure.

Safeguards: leaves product records and CMS schema untouched; backs up modified files;
refuses edits to unknown templates; supports --dry-run.
"""
import argparse
import json
from pathlib import Path
import sys

p = argparse.ArgumentParser()
p.add_argument('--root', default='.', help='Git repository root')
p.add_argument('--dry-run', action='store_true')
a = p.parse_args()
root = Path(a.root).resolve()
changes=[]
skips=[]

def replace_exact(rel, old, new, label):
    path=root/rel
    if not path.exists():
        skips.append(f'{label}: missing {rel}');return
    txt=path.read_text(encoding='utf-8')
    if old not in txt:
        skips.append(f'{label}: template differs, no changes made to {rel}');return
    updated=txt.replace(old,new,1)
    if not a.dry_run:
        backup=path.with_suffix(path.suffix+'.scenthunt-backup')
        if not backup.exists(): backup.write_text(txt,encoding='utf-8')
        path.write_text(updated,encoding='utf-8')
    changes.append(f'{label}: {rel}')

settings=root/'src/data/settings.json'
if settings.exists():
    try:
        raw=settings.read_text(encoding='utf-8'); data=json.loads(raw)
        updates={'brandName':'ScentHunt','tagline':'Explore. Wear. Discover.','minimumOrder':100,'deliveryFee':20,'freeDeliveryAt':150}
        before={k:data.get(k) for k in updates}
        data.update(updates)
        if before!={k:data[k] for k in updates}:
            if not a.dry_run:
                backup=settings.with_suffix('.json.scenthunt-backup')
                if not backup.exists(): backup.write_text(raw,encoding='utf-8')
                settings.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            changes.append('Brand and checkout thresholds: src/data/settings.json')
        else: skips.append('Settings already current')
    except (ValueError, OSError) as e: skips.append(f'Settings not modified: {e}')
else: skips.append('Settings file not found')

replace_exact('src/pages/index.astro',
    '<a class="button-dark" href="#collection">Explore the collection <span>↗</span></a><a class="text-link" href="#discover">Find your mood <span>→</span></a>',
    '<a class="button-dark" href="#collection">Explore the collection <span>↗</span></a><a class="button-outline" href="#collection" data-focus-product-search>⌕ Find a Perfume</a><a class="text-link" href="#discover">Find your mood <span>→</span></a>',
    'Visible search CTA next to Explore')
replace_exact('src/pages/index.astro',
    "document.querySelectorAll('[data-mood-shortcut]').forEach(el=>el.addEventListener('click'",
    "document.querySelectorAll('[data-focus-product-search]').forEach(el=>el.addEventListener('click',()=>setTimeout(()=>search?.focus(),80)));\ndocument.querySelectorAll('[data-mood-shortcut]').forEach(el=>el.addEventListener('click'",
    'Focus search input on CTA')
replace_exact('src/pages/perfumes/[slug].astro',
    '<div class="notes-grid">{p.notes.map((n,i)=><div><span>0{i+1}</span><b>{n}</b></div>)}</div>',
    '<div class="notes-grid">{p.notes.map(n=><div><b>{n}</b></div>)}</div>',
    'Unnumbered fragrance notes')
replace_exact('src/layouts/Base.astro',
    'aria-label="Modern Atelier homepage"',
    'aria-label="ScentHunt homepage"',
    'Header accessibility name')
replace_exact('src/layouts/Base.astro',
    '<span>modern <em>atelier</em><small>THE FRAGRANCE EDIT</small></span>',
    '<span>scent<em>hunt</em><small>EXPLORE. WEAR. DISCOVER.</small></span>',
    'ScentHunt header wordmark')
replace_exact('src/layouts/Base.astro',
    '<div class="footer-brand">modern <em>atelier</em> ✳</div>',
    '<div class="footer-brand">scent<em>hunt</em> ✳</div>',
    'ScentHunt footer wordmark')
replace_exact('src/layouts/Base.astro',
    '© {new Date().getFullYear()} Modern Atelier · UAE',
    '© {new Date().getFullYear()} ScentHunt · UAE',
    'ScentHunt copyright')
replace_exact('src/scripts/cart.js',
    "const key='modern-atelier-demo-cart-v1';",
    "const key='modern-atelier-demo-cart-v1'; // Retain storage key to preserve existing visitors' local carts.",
    'Preserve existing cart state')
replace_exact('src/scripts/cart.js',
    '`MODERN ATELIER — ORDER ENQUIRY`',
    '`SCENTHUNT — ORDER ENQUIRY`',
    'ScentHunt enquiry text')
print('ScentHunt guarded patch'+(' (DRY RUN)' if a.dry_run else ''))
for x in changes: print('UPDATED:',x)
for x in skips: print('SKIPPED:',x)
print('No product listings or CMS configuration were modified.')
if skips:
    print('Some changes skipped. Review skips before deployment; do not force-apply to different code.')
