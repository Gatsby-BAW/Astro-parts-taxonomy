# Astro Parts Ordering — automotive taxonomy draft

This directory contains the **review-only** mechanic-first navigation overlay. It does not change Shopify's upstream files, Astro-WebAdmin, or AWS.

## Scope
- Source: Shopify Product Taxonomy (MIT) at fork commit `cd90d2796a6cab4a8975ebb4e9832354752ee525`, source blob `52dc5e6635ffeede584239a5b711c03fe58c2aa1`.
- Fork VERSION at this commit is **2027-01-unstable**. The data is pinned by commit/blob SHA, not an assumption that `main` is a stable release.
- `automotive-navigation.json`: 19 proposed UI sections, 32 subgroups, 177 exact Shopify part categories and 38 proposed Astro specialist part categories.
- A `shopify:` entry preserves the original `source_id`, name, and optionally the upstream deeper descendants.
- An `astro:part/` entry is **proposed**, not already present in Shopify and not yet approved by the business.
- `fallback` exposes the existing Shopify motor-vehicle hierarchy for categories not curated into these main menus.
- Preserve the upstream [MIT license](../LICENSE) notice in derivative/distributed copies.

## How the UI should behave (subject to approval)
1. **Initial screen:** show VIN search / select saved vehicle / manual year-make-model-engine, plus a separate **exact part-number** search. Don't reveal category browsing or call suppliers until the vehicle is identified.
2. **Description search:** require vehicle details for vehicle-specific parts. Confirm unresolved engine, trim, axle, or brake configuration where necessary; VIN decoding alone cannot prove fitment.
3. **Categories:** after vehicle identification, show sections → subgroups → part types, expanding Shopify descendants as applicable.
4. **Search:** selecting a specific part type triggers targeted requests to **approved** supplier APIs only if they support targeted searches; do not fetch complete catalogs.
5. **Ranking:** group the same product (manufacturer + part number) from multiple suppliers; display roughly five verified compatible options across economy / standard / premium / OEM *when those classifications are supported*, then sort displayed options by current price ascending. Allow “more results.”
6. **Preferred brands:** tenant administrators manage company-wide preferences in Settings → Automotive → Parts Ordering; technicians may temporarily filter results without changing settings.
7. **Ordering:** price, available stock, shipping, order placement, tracking and interchange/fitment data must come from vendor APIs where permitted. Never imply all suppliers support every capability.
8. **Access:** the private Parts Ordering tab remains gated on the Astro application server for the approved Tom's Auto Works tenant; this public taxonomy fork contains no tenant IDs, credentials, or product quotes.

## Data/implementation boundaries
- These are **part types/categories**, NOT actual manufacturer part numbers, live inventory, commercial prices, or per-vehicle fitment.
- Do not add catalog results to the existing inventory stock ledger by searching; adding to estimates or ordering is a separate explicit action.
- Existing Astro PostgreSQL can store the selected taxonomy when approved; no new AWS database is needed.
- Supplier-to-Astro category mappings belong in the application and must account for supplier-specific filtering and license terms.
- Do not scrape suppliers or persist their product data contrary to their terms.
- The fork remains independent; **no automatic syncing or deployment to production**.
- The next step is review of these proposed menus and missing parts; do not merge this draft into `main` until approved.

## Run local validation
From the repo root: `python3 astro/validate_navigation.py` (Python standard library only).
