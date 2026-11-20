import settings from './data/settings.json';
export const currency = (n) => `AED ${Number(n).toFixed(0)}`;
export function availableVariants(p) {
  const values = [3,5,10].map(size => ({ sizeMl:size, price:Number(p[`price${size}Ml`]) }));
  const listed=values.filter(v=>Number.isFinite(v.price)&&v.price>0);
  if (!listed.some(v=>v.sizeMl===Number(p.sizeMl))) listed.push({sizeMl:Number(p.sizeMl),price:Number(p.price)});
  return listed.filter(v=>Number.isFinite(v.sizeMl)&&Number.isFinite(v.price)&&v.price>0).sort((a,b)=>a.sizeMl-b.sizeMl);
}
export function productEconomics(p, percent = p.promoPercent || 0) {
  const liquid = p.bottleCost / p.bottleMl * p.sizeMl / (1-settings.handlingLossRate);
  const price = p.price*(1-percent/100);
  const supplies = settings.atomizerCost + settings.perItemSupplies;
  const contribution = price - liquid - supplies;
  return { liquid, price, supplies, contribution, margin:price>0?contribution/price:0 };
}
export function promotionAllowed(p, pct) {
  const v = productEconomics(p, pct);
  // Product-level gate: delivery and order-level transaction fees are checked separately in cart economics.
  return pct>=0 && pct<=settings.maximumPromotionPercent && v.margin>=settings.minContributionMargin;
}
export function approvedPromotion(p) {
  const pct=Number(p.promoPercent)||0;
  if (!(pct>0 && pct<=settings.maximumPromotionPercent)) return 0;
  const variants=availableVariants(p);
  const safe=variants.every(v=>{
    const sale=v.price*(1-pct/100);
    const liquid=p.bottleCost/p.bottleMl*v.sizeMl/(1-settings.handlingLossRate);
    return sale>0 && (sale-liquid-settings.atomizerCost-settings.perItemSupplies)/sale>=settings.minContributionMargin;
  });
  return safe?pct:0;
}
export function orderEconomics(items, deliveryCharged) {
  const subtotal=items.reduce((a,it)=>a+it.price*it.qty,0);
  const liquid=items.reduce((a,it)=>a+it.liquid*it.qty,0);
  const packaging=items.reduce((a,it)=>a+settings.atomizerCost*it.qty+settings.perItemSupplies*it.qty,settings.orderPackaging);
  const pay=(subtotal+deliveryCharged)*settings.paymentFeePercent+settings.paymentFeeFixed;
  const fee=pay*(1+settings.paymentFeeVat);
  const contribution=subtotal+deliveryCharged-liquid-packaging-fee-settings.assumedCourierCost;
  return { subtotal, liquid, packaging, fee, contribution, margin:subtotal>0?contribution/subtotal:0 };
}
