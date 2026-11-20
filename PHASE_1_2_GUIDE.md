# ScentHunt Phase 1 + 2 update

## What changed

- Header reads **ScentHunt** (capital H); removed the unrelated star/asterisk favicon.
- Removed the unfulfilled "complimentary discovery guide" promise.
- Stronger manufacturer-brand typography (e.g. MANCERA) on product pages and catalogue cards.
- Improved product image, card actions, responsive spacing and keyboard focus.
- Existing CMS *individual JSON files* remain intact; all sizes remain 3, 5 and 10 ml only.
- New CMS records default to unpublished, pending review. Existing published products stay as-is.
- Empty or incomplete draft records no longer cause the catalogue to crash on missing notes.
- A local CSV import/validation tool adds many fragrance drafts, without overwriting existing products.

## Important: intended source version

Patch is based on the **Phase 2.2 source ZIP previously provided** (`scenthunt-phase22-source.zip`), NOT the original starter and NOT a fresh GitHub checkout. If your latest repository has changed, `git apply --check` may fail; do not force it. The user's Pages CMS files are not overwritten by this patch.

## Apply safely

```bash
git checkout main
git pull --ff-only origin main
git checkout -b feature/phase1-phase2-polish
git apply --check ~/Downloads/scenthunt-phase1-phase2.patch
git apply ~/Downloads/scenthunt-phase1-phase2.patch
python3 tools/fragrance_catalog.py validate --repo .
npm ci
npm run build
```

Review locally with `npm run dev`, especially home/catalogue, product page and cart; then commit and open a PR. A passing build alone does not verify browser interactions.

## Managing large catalogues

Existing records are stored separately in `src/data/fragrances/*.json`, edited individually via Pages CMS. New entries should remain hidden until images, stock, sizes and prices are verified.

For a batch, edit `tools/fragrance-import-template.csv` (or create a new CSV):

```bash
python3 tools/fragrance_catalog.py import-csv --repo . --csv tools/fragrance-import-template.csv
python3 tools/fragrance_catalog.py import-csv --repo . --csv tools/fragrance-import-template.csv --apply
python3 tools/fragrance_catalog.py validate --repo .
```

Rows must have `brand` and `name`. Optional fields include `category`, `family`, `mood`, `description`, `notes` (pipe separated), `color`, `bottleMl`, `bottleCost`, `stockMl`.

The importer produces draft JSON (all sizes disabled, all prices zero, `active: false`) and refuses to overwrite any existing slug. It **does not research** fragrance notes or generate/upload photos. Add verified official notes, licensed bottle photography, actual prices and stock in Pages CMS before publishing.

## Images

JSON files contain *paths* such as `/images/brand-perfume.webp`, not image bytes. Upload actual files using the Pages CMS media manager or into `public/images/`. Keep the matching case-sensitive filename. Existing Instant Crush artwork is preserved.

## Test-product failures

If Pages CMS saves a new draft but CI fails, click the failing GitHub check for the exact error. Use `tools/fragrance_catalog.py validate` to catch missing slug/filename mismatches and offered sizes without prices. Incomplete drafts are skipped or normalized safely at build time, but data errors still need correction before publishing.

## Limitations and next phase

This is a storefront and CMS workflow patch, not a secure checkout. Payment and live orders remain disabled pending approvals. This patch does not add photo generation or authentication.
