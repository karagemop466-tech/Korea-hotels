# Repo Review & Recommendations — 2026-08-09

Trip: **Seoul 8n → Gyeongju 6n → Busan 8n** (Oct 31 – Nov 22, 2026), with Cheonan / Daejeon
as alternates for the middle leg. 24 hotels published, all re-verified against official
sources on 2026-08-09.

---

## Part 1 — Repo review (what's strong, what's in the way)

### Strengths
- **Single source of truth**: `data/*.json` → `build.py` → `index.html`. No copy-paste drift
  between data and UI as long as everyone edits JSON only.
- **Real verification discipline**: `guide/verification-report-2026-08-09.md` caught serious
  issues (Accor codes pointing at hotels in France, a Marriott code pointing at the wrong
  Seoul hotel, dead domains, a false "7-min walk to KTX" claim). `data/excluded.json` keeps
  removals transparent. This is the best part of the repo — keep this culture.
- **Tooling exists**: `validate.py` (data contract), `audit_report.py` (reproducible summary),
  `build.py` (regeneration), `verification-checklist.md` (booking workflow).
- **Rich UI already**: city tabs, must-have filters, search, budget calculator, night-by-night
  planner, favorites, Leaflet map, deals/loyalty panels, 2–4 hotel comparison modal, decision
  shortlist, CSV/PDF-style export, localStorage persistence.

### Gaps & confirmed defects
| # | Finding | Evidence |
|---|---------|----------|
| G1 | **Gyeongju — a 6-night planned leg — has ZERO bookable hotels in the app.** All 5 candidates were excluded by the walk-to-station rule; Gyeongju has no subway and KTX arrives at Singyeongju, ~20 min out of town. | `data/hotels.json` (0 Gyeongju), `guide/verification-checklist.md` "Gyeongju exception" |
| G2 | **Confirmed rendering bug**: `renderBudget()` and `renderDecision()` display `h.price`, but **no hotel record has a `price` field** → "undefined/night" in the budget dropdown and decision shortlist. | `index.template.html` (renderBudget/renderDecision) vs all 24 records |
| G3 | Budget math uses only `priceFrom` (the most optimistic number) × nights. Ignores `priceTo`, taxes/fees, breakfast (ibis Styles: ₩26,000, flagged in the verification report), and the KTX estimate is hardcoded `36+8` with no source. | `renderBudget()` |
| G4 | Prices are a one-time snapshot (`pricingLastChecked: 2026-08-07`). No per-hotel freshness, no staleness badge, no place to log the live quotes the checklist tells you to capture. | `data/hotels.json → meta` |
| G5 | No booking-status or cancellation-deadline tracking, even though the checklist workflow says "book refundable now, recheck 30–45 days before arrival." Check-in is 2026-10-31 → recheck window is ~mid-September 2026. | `guide/verification-checklist.md` |
| G6 | Decision scorer is a fixed formula (`stars*22 − price*.12 − walk*.8 …`). No user weights, no "why did this win" explanation. | `renderDecision()` |
| G7 | URL rot already happened once (13 official links fixed on 2026-08-09). Nothing checks links automatically; `validate.py` never validates `officialUrl` format, field types, or coordinates. | verification report §1 |
| G8 | `itinerary.json` has `hotelChoice: null` per leg, but the UI never writes it — selections live only in browser localStorage and are lost on device change. | `data/itinerary.json` vs template LS usage |
| G9 | Guides can drift from data: `guide/gyeongju.md` recommends 5 hotels that the strict shortlist excludes — fine as research notes, but nothing marks them as "fails must-have" in the guide itself beyond prose. | `guide/gyeongju.md` |
| G10 | All prices USD; booking happens in KRW (and one breakfast fee is quoted in won). No conversion, no configurable rate. | `data/hotels.json` |

---

## Part 2 — Ten upgrades, ranked by impact on your *final decision*

### 1. Close the Gyeongju gap with a "transit-exception" tier (highest impact)
You cannot finalize 6 of 22 nights today. Add Gyeongju candidates under an explicit,
documented exception: new fields `transitException: true`, `transitPlan` (e.g. "KTX to
Singyeongju → taxi ~20 min ≈ ₩25,000–30,000"), verified official source per hotel, and a
visible ⚠️ badge in the UI. `validate.py` should *require* `transitPlan` whenever the
station rule is relaxed. This matches the escape hatch already written in
`guide/verification-checklist.md`. Feasibility is confirmed — see Part 3.

### 2. Fix the `price` display bug and lock the template↔data contract
Add a `price` string to every record (or change the template to compute
``$${priceFrom}–${priceTo}``), then extend `validate.py` to fail on any field the template
references that the data lacks. Two-line fix, one-hour hardening — and "undefined/night"
disappears from the two screens you use most when deciding.

### 3. True trip-cost calculator (decide on totals, not nightly rates)
Per leg, pick the **room** (not just the hotel); default to the mid-point of the range;
add structured fields `taxesFeesNote`, `breakfastPrice`, and a manual **live-quote override**
with `quoteDate`. Add a USD⇄KRW toggle with an editable exchange rate. Show per-leg totals
and the 22-night grand total side by side, including the KTX legs with a sourced fare
table in the data instead of a hardcoded `$44`.

### 4. Booking tracker with cancellation deadlines
Per leg: status (`researching → refundable booked → final booked`), booking channel,
confirmation ref, refundable-until date. Render a countdown against 2026-10-31 check-in
and the checklist's "recheck 30–45 days before" rule (≈ Sep 16 – Oct 1). This turns the
static checklist into the actual decision workflow, stored in `data/bookings.json` so it
syncs via the repo rather than dying in localStorage.

### 5. Decision matrix with your own weights + explanations
Replace the fixed formula with sliders (price / station walk / star level / laundry /
deal), show each pick's score breakdown ("#1 because: $135 avg, 2-min walk, 4★"),
and add a **"Make final pick for this leg"** button that the build step writes back into
`itinerary.json → hotelChoice`. Decision-making becomes transparent and the JSON stays the
source of truth.

### 6. Price freshness + quote log
Add per-hotel `verifiedAt`; surface a staleness badge in the UI (amber >14 days, red >30).
Add `data/quotes.json` (hotel, date, channel, room, total, refundable?) so your
"recheck before booking" evidence accumulates in the repo and the final decision is based
on *dated* numbers, not August estimates.

### 7. One-click verification deep links
Replace generic `officialUrl` links with booking-engine deep links that carry each leg's
actual dates (check-in/check-out/guests). Verifying bed type, bathroom, and total price
for your exact nights then takes one click per hotel — which is exactly what the checklist
demands before you commit.

### 8. CI: automated link health + validation
URL rot is proven (13 links fixed once). Add a GitHub Action: on every PR and weekly,
run `validate.py` plus a link checker (e.g. lychee) over every `officialUrl`/`compareUrl`,
and fail on rot. Extend `validate.py`: field types (`stationWalkTime` string format),
coordinate bounding box for Korea, currency whitelist, `transitException` ⇒ `transitPlan`
required (from upgrade 1).

### 9. Verification evidence on every card
The data model already has a `_verification` field (currently null on most records).
Populate it with `{officialUrlChecked, bedEvidence, bathEvidence, stationEvidence,
sourceDomain}` and render it as a "Verified 2026-08-09 · lottehotel.com" badge with a
hover detail. When you're at the final decision, *when* and *where* each fact was verified
should be visible without opening the markdown report.

### 10. Final-decision one-pager
The repo already has partial export (CSV / text / jsPDF). Upgrade it into a single
printable decision sheet: per leg — final pick, room, total cost, refundable-until,
official link, transit plan, and the runner-up. That is the document you sit down with
to make the call, and it's what falls out naturally once 1–9 are in place.

**Suggested order**: 2 → 1 → 4/5 (the actual decision workflow) → 3 → 6 → 9 → 7 → 8 → 10.

---

## Part 3 — Can we expand the search with real, verifiable official sources? **Yes.**

### The source ladder (ranked by trust)
1. **Chain/property official sites** — lottehotel.com, hilton.com, lahan.com, all.accor.com,
   wyndhamhotels.com, marriott.com/…/hyatt.com, shillahotels.com, toyoko-inn.com, plus
   independent official domains such as **commodorehotel.co.kr**.
2. **VISITKOREA** (english.visitkorea.or.kr) — the Korea Tourism Organization's official
   government-run directory; authoritative for existence, address, star class, and the
   property's official website. Ideal cross-check when a hotel has no English site of its own.
3. **OTAs (KAYAK / Trip.com / Booking / Google Hotels)** — use only for bed-type and price
   cross-checks, never as the primary source. That matches this repo's existing method.

### Feasibility confirmed this session (Gyeongju)
| Candidate | Verifiable official source found | Notes for your must-haves |
|---|---|---|
| **Commodore Hotel Gyeongju** | ✅ VISITKOREA official listing (422 Bomun-ro, Bomun resort complex) + official site commodorehotel.co.kr | Private bathrooms (separate toilet/shower) confirmed; 4★ class |
| **Hilton Gyeongju** | ✅ hilton.com/en/hotels/kyjgyhi | King rooms; live rates seen ~US$139+ on official channel |
| **Lahan Select Gyeongju** | ✅ lahan.com/gyeongju (official domain used by the Lahan chain) | "1 Double bed" room types confirmed; 745-room resort |
| **GG Hotel** | ⚠️ No official English site — OTA-verifiable only (standard double ~US$56–70) | Meets bed spec via OTA listings; weakest source tier |
| **The-K Gyeongju Hotel** | ✅ thek-hotel.co.kr via VISITKOREA official listing | 4★, Bomun Lake area |

**Conclusion**: the blocker for Gyeongju is **not** source verifiability — Hilton, Lahan,
Commodore, and The-K all have verifiable official pages. The blocker is only your
near-transit must-have (Gyeongju has no subway; Singyeongju KTX is ~20 min from town).
Two ways through, both legitimate:

- **A.** Adopt upgrade #1's transit-exception tier and publish the 3–4 verified candidates
  above with documented taxi/shuttle plans, or
- **B.** Keep the rule absolute and re-plan Gyeongju as day trips from Busan
  (Singyeongju is ~30 min by KTX from Busan) — then the decision tool should model that
  cost/time trade-off explicitly.

### Beyond Gyeongju
- **Cheonan**: 5 removed records could return as `transitException` entries — Shilla Stay
  Cheonan is fully official-verified and only failed on walk distance (the report itself
  calls it "the quality pick" with a taxi plan).
- **Seoul / Busan / Daejeon**: chains already trusted in this repo (L7, Nine Tree,
  Shilla Stay, Toyoko Inn, ibis) operate many more walk-to-station properties than are
  currently listed; these are low-effort additions using the exact 2026-08-09 verification
  method (official page → bed/bath/transit evidence → `excluded.json`-style audit trail).

### Recommended data-model additions to make expansion safe
```jsonc
{
  "transitException": true,
  "transitPlan": "KTX Singyeongju → taxi ~20 min (≈₩25–30k) or hotel shuttle",
  "_verification": {
    "checkedAt": "2026-08-09",
    "sourceDomain": "commodorehotel.co.kr",
    "existenceSource": "VISITKOREA vcontsId 99034",
    "bedEvidence": "official room page: 1 double bed",
    "bathEvidence": "official room page: private bathroom",
    "stationEvidence": "n/a — exception: taxi plan documented"
  }
}
```
Keep the pipeline unchanged: **research → verify official source → record evidence →
`validate.py` (extended) → `build.py`**. Every new record enters with the same audit trail
as the 2026-08-09 pass, so the shortlist stays as trustworthy as it is today.
