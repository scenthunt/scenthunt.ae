// Vite bundles each Pages CMS fragrance record at build time.
// Each file is independently editable by Pages CMS.
const entries = import.meta.glob('./fragrances/*.json', { eager: true, import: 'default' });
export const products = Object.values(entries).sort((a, b) =>
  `${a.brand} ${a.name}`.localeCompare(`${b.brand} ${b.name}`)
);
