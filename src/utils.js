import settings from './data/settings.json';
export const currency = (n) => `AED ${Number(n).toFixed(0)}`;
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
export function orderEconomics(items, deliveryCharged) {
  const subtotal=items.reduce((a,it)=>a+it.price*it.qty,0);
  const liquid=items.reduce((a,it)=>a+it.liquid*it.qty,0);
  const packaging=items.reduce((a,it)=>a+settings.atomizerCost*it.qty+settings.perItemSupplies*it.qty,settings.orderPackaging);
  const pay=(subtotal+deliveryCharged)*settings.paymentFeePercent+settings.paymentFeeFixed;
  const fee=pay*(1+settings.paymentFeeVat);
  const contribution=subtotal+deliveryCharged-liquid-packaging-fee-settings.assumedCourierCost;
  return { subtotal, liquid, packaging, fee, contribution, margin:subtotal>0?contribution/subtotal:0 };
}
