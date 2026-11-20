# ScentHead/ScentHunt storefront phase 2

This package is based on the last uploaded `scenthunt.ae-main.zip` plus the earlier improvement patch. The GitHub head could not be accessed here; compare changes before merging because Pages CMS may have updated the remote since this snapshot.

## What changed
- Header wordmark displays **ScentHead** as requested. Project identifiers, SEO and footer continue to say **ScentHunt**; decide whether this is a rename before launch.
- Pages CMS now edits **one JSON record per fragrance** under `src/data/fragrances/` (searchable/sortable collection), instead of one huge `products.json` file.
- Existing 8 fragrances were migrated with their notes, images, costs, and stock, and the original `src/data/products.json` was kept as a backup, but **no longer drives the site**. Do not edit that legacy file.
- Categories are derived from the `category` field, and price/stock from each independent fragrance file.
- Pages CMS has clear **Offer 3 ml, Offer 5 ml, Offer 10 ml** toggles and price fields. A size is offered only when enabled and has a positive price; stock must also be sufficient.
- Instant Crush has **illustrative** 3/5/10 ml choices (AED 25/39/70), edit them before sales.
- Added `FragranceArt.astro` to display either `artwork` (finished single composite), or ingredient background + bottle cutout, or a neutral bottle photo fallback. Only Instant Crush has a sample artistic ingredient background and genuine bottle cutout. No general purpose automatic note-photo scraper or AI generator has been implemented; artwork for new fragrances still needs a curated ingredient image or custom composite.

## Safe migration instructions
1. Save a backup of your current Pages CMS records from the `main` branch before replacing any `src/data/fragrances` files.
2. Compare the package with your latest GitHub checkout. If CMS edits happened after the uploaded ZIP, copy your latest `src/data/products.json` into this package and run `python3 tools/sync_legacy_catalog.py` BEFORE switching CMS configuration; it imports newer notes, images and prices into the individual fragrance files. Review `git diff` afterwards.
3. Work in a new feature branch. Copy the changed website source and `public/images` assets, not `node_modules` or `dist`.
4. Run `npm ci` then `npm run build`. Check Instant Crush at `/perfumes/mancera-instant-crush/` and the size-aware cart; `npm run build` could not be run in the package-generation environment because npm dependencies were unavailable.
5. Confirm Pages CMS shows **Fragrances — one record per perfume**; verify adding a test fragrance updates the collection and creates a searchable product.
6. Only then create and merge your PR.

## Important remaining work
- Validate Pages CMS migration on the live repository.
- Validate contrast and responsive layouts on actual devices.
- Improve the background/mask cutout quality and provide a photo/ingredient library for all fragrances.
- Real checkout, payment and user data collection remain disabled pending required approvals.
