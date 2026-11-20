# ScentHunt — update from uploaded repository snapshot

Source: `scenthunt.ae-main.zip` supplied on 20 November 2026. Your `src/data/products.json` and `public/images/*` are left untouched.

## Included

- ScentHunt branding and tagline, without changing the underlying editorial art direction.
- New shop policy in `settings.json`: minimum AED 100, delivery AED 20 below AED 150, free delivery from AED 150. All remain preview-only while `acceptOrders` is false.
- Hero “Find a Perfume” button and header search link that focus the existing catalogue search.
- Search matches brand, name, fragrance family and note text; existing category filtering is already automatic from the `category` property in Pages CMS.
- Unnumbered scent notes.
- Optional 3 ml / 5 ml / 10 ml price fields in Pages CMS and size selector on product detail pages.
- Cart tracks fragrance + size, calculates stock consumption in millilitres across sizes, and prices the selected variant.
- Promotional discount is applied only when **all enabled size variants** meet the product contribution threshold.

## IMPORTANT: enabling additional sizes

The existing CMS entries carry **one** valid decant price/size. We did **not invent prices** for additional sizes. In Pages CMS, enter `price3Ml`, `price5Ml`, and/or `price10Ml` as positive AED prices to offer those sizes. Leave unused fields at 0. The existing `sizeMl` + `price` remains a fallback until you migrate each product. For consistency, set the price field matching your existing size to its existing price.

## Not included

- Automated composition of actual ingredient photographs with the bottle. That requires rights-cleared ingredient assets, source bottle cutouts, and a compositing pipeline. Uploaded white-background bottle photos remain visibly white; this release avoids claiming to automatically blend them.
- Live orders, user sign-up, payment, stock reservations, or Ziina backend. The store remains a demo with orders disabled.
- Automatic translation or external Fragrantica scraping.

## Build and release

1. Work on a new branch and back up CMS data.
2. `npm ci` and `npm run build` on your Mac.
3. Test adding different sizes to the cart, quantity limits, categories, search, delivery thresholds, and CMS editing.
4. Push the tested branch, then merge to `main` to trigger Cloudflare.

The authoring environment could not complete `npm ci` because package download stalled. Source JavaScript syntax and JSON checks passed, **but a full Astro production build has not been verified in this environment**.
