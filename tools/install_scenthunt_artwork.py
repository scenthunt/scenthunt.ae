#!/usr/bin/env python3
"""Install approved ScentHunt 14-fragrance artwork without changing prices or stock.

Run from your repository: python3 tools/install_scenthunt_artwork.py --repo .
Then add --apply after reviewing the planned changes.
"""
from pathlib import Path
import argparse,json,sys

ARTWORKS = [
 'ahmed-al-maghribi-marj',
 'ahmed-al-maghribi-summer-oud',
 'al-haramain-amber-oud-gold-edition',
 'alezz-oud-hersh-lahab',
 'armaf-club-de-nuit-untold',
 'bentley-for-men-absolute',
 'davidoff-cool-water-edt',
 'faiz-niche-silk-route',
 'lattafa-asad',
 'lattafa-khamrah',
 'maison-alhambra-avant',
 'mancera-cedrat-boise',
 'sasan-24',
 'versace-dylan-blue-pour-homme',
]
ALIASES = {'davidoff-cool-water-edt': ['davidoff-cool-watermelon']}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo',default='.',help='Your ScentHunt repo root')
    ap.add_argument('--apply',action='store_true',help='Write the artwork path into existing JSON records')
    ap.add_argument('--replace-existing',action='store_true',help='Also replace a previously set artwork value')
    args=ap.parse_args()
    repo=Path(args.repo).resolve()
    records=repo/'src/data/fragrances'
    assets=repo/'public/images'
    if not records.is_dir() or not assets.is_dir():
        sys.exit('ERROR: --repo must point at the ScentHunt website (src/data/fragrances and public/images required).')
    processed=skipped=errors=0
    for slug in ARTWORKS:
        asset=assets/f'{slug}-artwork.webp'
        record=None
        for candidate in [slug]+ALIASES.get(slug,[]):
            p=records/f'{candidate}.json'
            if p.is_file():
                record=p;break
        if not asset.is_file():
            print(f'ERROR {slug}: artwork file not found: {asset}')
            errors+=1;continue
        if record is None:
            print(f'SKIP  {slug}: no matching fragrance JSON found')
            skipped+=1;continue
        try:
            data=json.loads(record.read_text(encoding='utf-8'))
            if not isinstance(data,dict):raise ValueError('JSON must be an object')
        except Exception as exc:
            print(f'ERROR {record.name}: {exc}')
            errors+=1;continue
        value='/images/'+asset.name
        old=data.get('artwork','')
        if old and old!=value and not args.replace_existing:
            print(f'SKIP  {record.name}: existing artwork {old!r} (use --replace-existing to override)')
            skipped+=1;continue
        if old==value:
            print(f'OK    {record.name}: already points at {value}')
            processed+=1;continue
        print(f'{"WRITE" if args.apply else "PLAN "} {record.name}: artwork {old!r} -> {value!r}')
        if args.apply:
            data['artwork']=value
            record.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        processed+=1
    print(f'\nSummary: {processed} matched, {skipped} skipped, {errors} errors.')
    if not args.apply:print('Dry run only. Re-run with --apply to save the JSON changes.')
    if errors:sys.exit(1)

if __name__=='__main__':main()
