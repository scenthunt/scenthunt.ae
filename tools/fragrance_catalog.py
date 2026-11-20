#!/usr/bin/env python3
"""Safe ScentHunt catalogue helper: validate, prepare CSV drafts, and inspect images.
No credentials, network calls, overwrite or auto-publication.
"""
import argparse,csv,json,re,sys
from pathlib import Path

CATEGORIES={'middle-eastern','designer','niche'}
MOODS={'Everyday','Fresh days','After dark','Cosy nights'}
COLORS={'peach','sage','lilac','blue','honey','terracotta','rose'}
SIZES=(3,5,10)

def slugify(value):
    return re.sub(r'-+','-',re.sub(r'[^a-z0-9]+','-',value.lower())).strip('-')

def draft(row):
    brand=(row.get('brand') or '').strip()
    name=(row.get('name') or '').strip()
    slug=slugify(row.get('slug') or f'{brand}-{name}')
    if not brand or not name or not slug:
        raise ValueError('brand and name are required')
    category=(row.get('category') or 'designer').strip().lower()
    if category not in CATEGORIES:raise ValueError(f'{slug}: invalid category {category!r}')
    mood=(row.get('mood') or 'Everyday').strip()
    if mood not in MOODS:raise ValueError(f'{slug}: invalid mood {mood!r}')
    color=(row.get('color') or 'peach').strip()
    if color not in COLORS:raise ValueError(f'{slug}: invalid color {color!r}')
    def number(field):
        v=(row.get(field) or '').strip()
        try:return float(v) if v else 0
        except ValueError: raise ValueError(f'{slug}: invalid {field}: {v}')
    notes=[x.strip() for x in (row.get('notes') or '').split('|') if x.strip()]
    d={"slug":slug,"name":name,"brand":brand,"active":False,"category":category,
       "family":(row.get('family') or '').strip(),"mood":mood,"description":(row.get('description') or '').strip(),"notes":notes,
       "stockMl":number('stockMl'),"bottleMl":number('bottleMl'),"bottleCost":number('bottleCost'),
       "offer3Ml":False,"price3Ml":0,"offer5Ml":False,"price5Ml":0,"offer10Ml":False,"price10Ml":0,
       "promoPercent":0,"color":color,"image":"","artwork":"","ingredientBackground":"","bottleCutout":"","featured":False}
    return d

def validate(path):
    errors=[];warnings=[];seen=set()
    for file in sorted(path.glob('*.json')):
        try:d=json.loads(file.read_text(encoding='utf-8'))
        except Exception as exc: errors.append(f'{file.name}: invalid JSON: {exc}');continue
        for key in ['slug','name','brand']:
            if not isinstance(d.get(key),str) or not d[key].strip():errors.append(f'{file.name}: missing {key}')
        if d.get('slug')!=file.stem:errors.append(f'{file.name}: slug must match filename')
        if d.get('slug') in seen:errors.append(f'{file.name}: duplicate slug')
        seen.add(d.get('slug'))
        if d.get('category') not in CATEGORIES:warnings.append(f'{file.name}: choose a valid category')
        if d.get('mood') not in MOODS:warnings.append(f'{file.name}: choose a valid mood')
        if not isinstance(d.get('notes',[]),list):errors.append(f'{file.name}: notes must be a list')
        for size in SIZES:
            offer=d.get(f'offer{size}Ml')
            price=d.get(f'price{size}Ml',0)
            if offer is True and (not isinstance(price,(float,int)) or price<=0):errors.append(f'{file.name}: {size} ml offered without positive price')
        if d.get('active') is True:
            if not d.get('description'):warnings.append(f'{file.name}: public record has no description')
            if not d.get('image') and not d.get('artwork') and not (d.get('bottleCutout') and d.get('ingredientBackground')):warnings.append(f'{file.name}: no bottle image')
            if not any(d.get(f'offer{size}Ml') and (d.get(f'price{size}Ml') or 0)>0 for size in SIZES) and not d.get('price'):warnings.append(f'{file.name}: public record has no priced decant sizes')
    return errors,warnings

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('action',choices=['validate','import-csv'])
    a.add_argument('--repo',default='.',help='Root directory of ScentHunt repository')
    a.add_argument('--csv',help='CSV with columns brand,name,category,notes,...')
    a.add_argument('--apply',action='store_true',help='Write new draft files; existing records are NEVER overwritten')
    args=a.parse_args();repo=Path(args.repo).resolve();folder=repo/'src/data/fragrances'
    if not folder.is_dir():sys.exit(f'ERROR: {folder} missing; pass --repo path to repository root')
    if args.action=='validate':
        errs,warns=validate(folder)
        for x in warns:print('WARN:',x)
        for x in errs:print('ERROR:',x)
        print(f'Checked {len(list(folder.glob("*.json")))} fragrance files; {len(errs)} errors, {len(warns)} warnings.')
        sys.exit(1 if errs else 0)
    if not args.csv:sys.exit('ERROR: --csv is required')
    source=Path(args.csv)
    if not source.is_file():sys.exit(f'ERROR: {source} not found')
    created=skipped=0;duplicate=set()
    with source.open(newline='',encoding='utf-8-sig') as inp:
        rows=csv.DictReader(inp)
        if not {'brand','name'}.issubset(set(rows.fieldnames or [])):sys.exit('CSV requires brand and name columns')
        for n,row in enumerate(rows,2):
            try:d=draft(row)
            except ValueError as exc:sys.exit(f'CSV line {n}: {exc}')
            target=folder/(d['slug']+'.json')
            if target.exists() or d['slug'] in duplicate:
                print('SKIP (exists):',d['slug']);skipped+=1;continue
            duplicate.add(d['slug']);print(('WRITE' if args.apply else 'WOULD CREATE'),target.name);created+=1
            if args.apply:
                # Exclusive create protects against accidental overwrites even during races.
                with target.open('x',encoding='utf-8') as dest:json.dump(d,dest,indent=2,ensure_ascii=False);dest.write('\n')
    print(f'{created} new drafts, {skipped} skipped. '+('All new drafts have active=false.' if args.apply else 'Dry run only; add --apply to write files.'))

if __name__=='__main__':main()
