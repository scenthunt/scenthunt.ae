# ScentHunt — responsive visual refinement

Based on `scenthunt.ae-main-2.zip` uploaded November 20, 2026.

## Changes
- Consistent visible wordmark: **ScentHunt** in header and footer.
- Square image frames on both the catalogue and product page, matching the square ingredient artwork source.
- No `object-fit: cover` cropping on the featured product artwork; transparent bottle layer and ingredient layer use a full square area.
- Rounded artwork corners, a subtle shadow and warm radial gradient background.
- Removed decorative circles on catalogue thumbnails; consistent card spacing.
- Replaced green placeholder symbol with understated S/H typographic fallback and fragrance name.
- No changes to Pages CMS, fragrance JSON files, variants, prices or orders.

## Deployment
1. Apply to a branch from current main, preserving any more recent CMS edits.
2. Run `npm ci` (requires a supported Node version), then `npm run build` on your Mac.
3. Preview the catalogue and product pages at mobile and desktop widths.
4. Commit, push and merge only after build and review.

This environment could not finish npm dependency installation, so the Astro production build remains **unverified** here. The image-layout modifications are CSS/component updates only.
