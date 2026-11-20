// Individual JSON files are the source of truth. New CMS drafts may be incomplete.
// Keep drafts unpublished until reviewed; never invent prices, stock or notes.
const entries = import.meta.glob('./fragrances/*.json', { eager: true, import: 'default' });
const validCategories = new Set(['middle-eastern', 'designer', 'niche']);
const validMoods = new Set(['Everyday', 'Fresh days', 'After dark', 'Cosy nights']);
const validColors = new Set(['peach', 'sage', 'lilac', 'blue', 'honey', 'terracotta', 'rose']);
const numeric = value => Number.isFinite(Number(value)) ? Number(value) : 0;
export function normalizeProduct(raw, filename = '') {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return null;
  const slug = String(raw.slug || filename.replace(/\.json$/i, '')).trim();
  const name = String(raw.name || '').trim();
  const brand = String(raw.brand || '').trim();
  if (!slug || !name || !brand || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) return null;
  const notes = Array.isArray(raw.notes) ? raw.notes.filter(x => typeof x === 'string').map(x => x.trim()).filter(Boolean) : [];
  return {
    ...raw, slug, name, brand, notes,
    category: validCategories.has(raw.category) ? raw.category : 'designer',
    mood: validMoods.has(raw.mood) ? raw.mood : 'Everyday',
    color: validColors.has(raw.color) ? raw.color : 'peach',
    family: String(raw.family || 'Fragrance discovery').trim(),
    description: String(raw.description || '').trim(),
    image: String(raw.image || ''), artwork: String(raw.artwork || ''),
    ingredientBackground: String(raw.ingredientBackground || ''),
    bottleCutout: String(raw.bottleCutout || ''),
    stockMl: Math.max(0, numeric(raw.stockMl)),
    bottleMl: Math.max(0, numeric(raw.bottleMl)),
    bottleCost: Math.max(0, numeric(raw.bottleCost)),
    sizeMl: numeric(raw.sizeMl), price: Math.max(0, numeric(raw.price)),
    price3Ml: Math.max(0, numeric(raw.price3Ml)),
    price5Ml: Math.max(0, numeric(raw.price5Ml)),
    price10Ml: Math.max(0, numeric(raw.price10Ml)),
    promoPercent: Math.max(0, numeric(raw.promoPercent)),
    active: raw.active === true, featured: raw.featured === true,
  };
}
export const products = Object.entries(entries)
  .map(([file, value]) => normalizeProduct(value, file.split('/').pop()))
  .filter(Boolean)
  .sort((a, b) => `${a.brand} ${a.name}`.localeCompare(`${b.brand} ${b.name}`));
