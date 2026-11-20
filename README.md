# Modern Atelier — Pre-launch storefront prototype

Original, mobile-first Astro + TypeScript-ready storefront for a small Abu Dhabi perfume-decant project. This is a **working catalogue and cart demo**, NOT a production-ready, legally approved e-commerce shop.

## What works
- Responsive design, fragrance filters, keyword search, mood-based navigation.
- Individual static product pages with SEO title/description and Product JSON-LD.
- Custom cart, quantity edits, AED 120 minimum, AED 15 delivery, free from AED 200 (all configurable).
- Product-level promotional percentage only if a >=30% variable contribution margin survives the promotion, with AED 3 atomizers and 3% transfer loss modelled.
- Inventory availability in ml; sold-out products cannot be added. There is **no live order deduction or reservation**.
- Pages CMS configuration for a GitHub-based catalogue editor, including image uploads, stock and promotional discounts.
- Payment collection **disabled**. WhatsApp enquiry feature remains disabled by default.

## Run locally
```bash
npm install
npm run dev
```
Open http://localhost:4321. Production build: `npm run build` (output `dist/`).

## Deploy to Cloudflare Pages (static)
1. Create a private GitHub repository and upload this project.
2. In Cloudflare Workers & Pages, connect the GitHub repo as a Pages project.
3. Build command: `npm run build`; output directory: `dist`. Node 20+.
4. Configure `PUBLIC_SITE_URL=https://your-actual-domain.example` in build environment variables, then redeploy.
5. Pre-launch: `public/robots.txt` blocks indexing and pages currently use noindex. **Do not remove pre-launch protections until all content, image rights, compliance and actual ordering are approved.**

## Edit catalogue with Pages CMS
Login at https://app.pagescms.org with your GitHub account and grant repository access. `.pages.yml` maps the `src/data/products.json` root object and `src/data/settings.json` to form fields. Check the configuration in the actual editor, and adjust its field schema if required by future CMS updates. Updating via CMS commits to GitHub, triggering Cloudflare rebuild.

In `src/data/products.json`, every fragrance is a **sample listing with illustrative acquisition costs/prices**. `image` is empty, so bottle visuals are clearly labelled illustration placeholders. Upload licensed original bottle or bottle-plus-notes composite images to `public/images`, set `image` to `/images/your-file.webp`, and verify product/notes against sources you can legally reuse. For a 3 ml and 5 ml option of the *same* fragrance, use separate product entries and unique slugs in this first version.

## Pricing and 20% promotions
`src/data/settings.json` controls `atomizerCost: 3`, `perItemSupplies: .7`, handling loss 3%, estimated courier 25, min contribution margin 30%, max promotion 20%. `promoPercent` on a product is **only applied if the product's discounted price meets the product-level margin floor**. Otherwise it is ignored. The current floor is a screening rule, NOT a guarantee the final order makes 30% after shipping, payment fees, packaging, tax, returns, advertising, staff time or legal costs. In a small business the economics should also be reviewed across the entire cart before a promotion is published.

Example: 100 ml bottle purchased for AED 120; 5 ml sample sold for AED 21. Cost of liquid including 3% loss = 6.19; atomizer + supplies = AED 3.70. With 20% off, sale price AED 16.80 and product contribution AED 6.91 (41% of revenue, **before order-level fees**), thus passes. A higher-cost perfume may fail and retain regular price.

## Order enquiries and payments
Leave `acceptOrders:false` until licensing, handling/shipping and merchant approval are obtained. Once confirmed, set `whatsappNumber` in international digits (e.g. 971...) and `acceptOrders:true` for customer enquiry handoff only. **Do not place Ziina API keys in browser code or GitHub.** Integrated payments need a backend payment-intent function, secure signature/status validation, idempotent order records, and stock management. Payment links may be generated manually in Ziina and shared after order confirmation, if approved for this activity.

## SEO launch checklist
- Replace `example.pages.dev` with actual verified URL.
- Replace product samples and illustrations with authorised bottle photos + original note artwork.
- Add proper shipping/returns/contact and company details, verify exact inventory and product variant info.
- Remove `noindex` and change robots to `Allow: /` **only when the shop may legally operate**.
- Submit sitemap to Google Search Console; audit canonical URLs, structured data and Core Web Vitals.
- Do not promise indexing or recommendations by AI search platforms.

## Limits of this version
No authentication, checkout/payment API, real-time DB, order management, inventory reservation, or working admin preview inside the website. Pages CMS provides an external GitHub editor. Photos are not generated from internet sources. No service or accounts have been deployed/connected.
