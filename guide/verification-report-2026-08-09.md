# Official-Source Verification Report — 2026-08-09

**Scope:** all 29 hotel records previously published in `data/hotels.json`.
**Method:** each record's official URL was opened and checked; where the link was dead or
mis-pointed, the hotel's official page was re-located via the chain's official domain or
authoritative listings (Accor, Marriott, Hyatt, Wyndham, Lotte, Shilla, Toyoko Inn,
VISITKOREA). Bed configuration, private bathroom, check-in/out, and station proximity were
re-checked against the official page wherever available.
**Result:** **24 records verified & kept · 5 records removed** (moved to `data/excluded.json`)
· **13 official URLs fixed or replaced.**

Our three non-negotiable requirements (per README):

1. **One single bed** — queen (~150 cm) or larger, one unit, not two beds pushed together.
2. **Private en-suite bathroom.**
3. **Walking distance to a subway or KTX station** (1–15 min walk per `guide/room-match.md`).

---

## 1. Verdicts at a glance

### ✅ Seoul — 8/8 verified

| Hotel | Exists & official page | Bed | Bath | Transit | Fixes applied |
|-------|------------------------|-----|------|---------|---------------|
| L7 Myeongdong by LOTTE | ✅ lottehotel.com/myeongdong-l7 (15:00/11:00 confirmed) | ✅ queen rooms | ✅ | ✅ ~2 min Myeongdong Stn | de-duplicated promo lines |
| Nine Tree by Parnas Myeongdong 1 | ✅ **URL fixed** → ninetreehotels.com/nth1 (old link 404) | ✅ Standard Double | ✅ (coin laundry on site) | ✅ ~1–2 min Myeongdong Stn | URL, check-out 12:00 |
| ibis Styles Ambassador Myeongdong | ✅ **URL fixed** → all.accor.com/hotel/9771 (old code 1976 = a Mercure in France!) | ⚠️ official lists **"1 double bed"** — confirm width at booking | ✅ paid coin laundry | ✅ 400 m/6 min Myeongdong (official) | URL, stars 3→4 (official), check-in 14:00, **breakfast is ₩26,000 — NOT free**, laundry true |
| ibis Ambassador Insadong (renovated) | ✅ **URL fixed** → all.accor.com/hotel/8002 (old code 1888 = a Mercure in Bourges!) | ✅ | ✅ coin laundry + hot bath | ✅ ~4 min Jongno / ~5 min Anguk | URL, stars 4→3 (official), check-in 14:00 |
| Four Seasons Seoul | ✅ fourseasons.com/seoul | ✅ **Deluxe = one KING bed (official)** — was listed as queen | ✅ | ✅ ~5 min Gwanghwamun | Deluxe room bedType queen→king |
| Fairmont Ambassador Seoul | ✅ URL canonicalized → fairmont.com/en/hotels/seoul/fairmont-ambassador-seoul.html | ✅ Deluxe King | ✅ | ✅ Yeouinaru Stn | URL |
| Hotel Skypark Myeongdong 3 | ✅ skyparkhotel.com | ✅ | ✅ | ✅ **directly at Myeongdong Stn Exit 9 (~1 min)** | walk time corrected (5 min → 1–2 min) |
| L'Escape (Luxury Collection) | ✅ **URL fixed** → marriott.com SELLM (old link used code SELAK = THE PLAZA Seoul!) | ✅ king | ✅ | ✅ Hoehyeon/Myeongdong | URL, check-out 11:00 (official) |

### ✅ Busan — 7/7 verified

| Hotel | Exists & official page | Bed | Bath | Transit | Fixes applied |
|-------|------------------------|-----|------|---------|---------------|
| Shilla Stay Haeundae | ✅ URL canonicalized → shillahotels.com/en/shillastay/haeundae (shillastay.com redirects; 407 rooms, laundry room) | ✅ | ✅ | ✅ 5–9 min Haeundae Stn | URL, promos tidied |
| L7 Haeundae by LOTTE | ✅ lottehotel.com/haeundae-l7 (opened June 2024 confirmed) | ✅ | ✅ | ✅ ~10 min Haeundae Stn | none |
| ASTI Hotel Busan Station | ✅ **URL fixed** → en.astihotel.co.kr (astihotel.com is parked/expired) | ✅ double/king | ✅ | ✅ **"1 minute from Busan station" (official)** | URL, check-out 11:00 |
| Grand Josun Busan | ✅ **URL fixed** → gjb.josunhotel.com (josun.com is a dead domain — HTTP 500) | ✅ | ✅ | ✅ 7–10 min Haeundae Stn | URL |
| Park Hyatt Busan | ✅ **URL fixed** → hyatt.com/park-hyatt/en-US/busph-park-hyatt-busan (old link "Not Found") | ✅ king | ✅ | ✅ ~8 min Dongbaek Stn | URL, check-out 11:00 (official) |
| Toyoko Inn Busan Haeundae 2 | ✅ toyoko-inn.com/eng/search/detail/00256 — fully confirmed (free breakfast, unit bath, laundromat; 15:00/10:00 matches record) | ✅ double | ✅ | ✅ 10 min Haeundae Stn Exit 5 (official) | walk time 8 → 10 min (official) |
| Ramada Encore by Wyndham Haeundae | ✅ wyndhamhotels.com page loads | ✅ | ✅ | ✅ Haeundae area | name corrected (official drops "Busan") |

### ⚠️ Cheonan — 2/7 verified · 5 removed

| Hotel | Verdict | Evidence |
|-------|---------|----------|
| Ramada Encore by Wyndham CheonAn | ✅ **kept** — official Wyndham page loads; real rail link is **Bongmyeong Stn ~750 m / 9 min**, not "10-min walk to Cheonan Station" (~2 km). Record corrected. | wyndhamhotels.com; Trip.com & MakeMyTrip station distances |
| Cheonan Brown Dot Hotel Cheonan Station | ✅ **kept** — property real (7-1 Keunsijang-gil; private bathrooms); **0.86 km / ~11 min to Cheonan Stn**. Chain site browndot.co.kr is offline (hosting error) → book via OTA. | Trip.com / Tripadvisor listings |
| Shilla Stay Cheonan | ❌ **removed** — hotel fully verified (177 Dongseo-daero; coin laundry; official page) but **~1.9 km ≈ 25-min walk to Cheonan Stn**, 15-min *drive* to KTX. Fails walk rule. Best Cheonan hotel by quality — re-add only with a documented taxi plan. | shillahotels.com; address/distance measured |
| ON City Hotel | ❌ **removed** — real hotel (105 Buldang 4-ro), but Buldang-dong is **~3.5 km from KTX, ~3 km from Cheonan Stn** (VISITKOREA: "5-minute **drive** from KTX"). Claimed "7-min walk" was false. | VISITKOREA official listing |
| Sono Belle Cheonan | ❌ **removed** — Tedin/Ocean-Adventure water-park resort **~11 km from KTX**; no rail access on foot. Also OTA-rated 3★, not 4★. | VISITKOREA; sonohotelsresorts.com |
| Best Western Asan Hotel | ❌ **removed** — now *SureStay Plus by Best Western Asan* in Tangjeong, **~6 km (3.7 mi) from Cheonan-Asan KTX**. "5-min walk to KTX" was false; bestwestern.com link returns an error page. | Booking.com; bestwestern.com error page |
| The Mains Hotel | ❌ **removed** — real (34 Cheongsu 11-ro) but **~2.7 km from Cheonan Stn (~30+ min walk)**; official URL wrongly pointed to shillahotels.com; no official site exists. | Booking.com / Tripadvisor |

### ✅ Daejeon — 7/7 verified

| Hotel | Exists & official page | Bed | Bath | Transit | Fixes applied |
|-------|------------------------|-----|------|---------|---------------|
| Toyoko Inn Daejeon Government Complex | ✅ **URL fixed** → toyoko-inn.com/eng/search/detail/00234 (old code 00235 deleted page) | ✅ | ✅ shower/tub combo (official) | ✅ Gov. Complex Stn Exit 4 (~4 min, official access guide) | URL, station text (was wrongly "Daejeon Station") |
| Ramada by Wyndham Daejeon | ✅ wyndhamhotels.com page loads | ✅ | ✅ | ✅ **3 min to Yuseong Spa Stn** — record wrongly said "8 min to Daejeon Station" (it's 15 km away in Yuseong-gu) | area/station/fitReason |
| LOTTE City Hotel Daejeon | ✅ lottehotel.com (33 Expo-ro 123beon-gil, before Convention Center) | ✅ | ✅ | ⚠️ ~12–15 min City Hall Stn — **edge of the 15-min rule; verify walking route** | label, walk note |
| Benikea Daelim Hotel | ✅ benikea.com lists 베니키아 호텔 대림 | ✅ | ✅ | ✅ **Jungangno Stn ~4 min**; KTX one stop (~1.2 km) — "2–5 min to Daejeon Station" claim fixed | area/station/highlights |
| Hotel Stendhal | ✅ **URL fixed** → stendhalhotel.co.kr (old link pointed to a different hotel, interciti.co.kr) | ✅ | ✅ separate tub/shower | ✅ ~7 min Yuseong Oncheon Stn | URL, geo, station |
| Hotel Interciti | ✅ interciti.co.kr loads with live booking engine; open & renovated 2023 | ✅ | ✅ | ✅ ~5 min Yuseong Oncheon Stn | geo, station |
| Aank Air Hotel Daejeon Station | ✅ verified via Expedia/Hotels.com/Trip.com; no own site (OTA-first brand) — link kept as labelled | ✅ | ✅ | ✅ **Jungangno Stn 270 m**, KTX 720 m | station text fixed (was generic) |

---

## 2. Corrections applied to the repo

**Data (`data/hotels.json`, rebuilt `index.html`)**
- 5 failing records moved to **`data/excluded.json`** with reasons + evidence (all were Cheonan entries failing requirement 3).
- **13 official URLs fixed/replaced:** Nine Tree (404), ibis Styles (wrong hotel), ibis Insadong (wrong hotel), L'Escape (wrong hotel — code SELAK→SELLM), Shilla Stay Haeundae (redirect), ASTI (parked domain), Grand Josun (dead domain), Park Hyatt (broken path), Toyoko Daejeon (dead code), Brown Dot (offline chain site → OTA), Stendhal (wrong hotel's domain), Fairmont (canonical), Lotte City label.
- Wrong station claims corrected: Ramada Daejeon (Daejeon Stn → Yuseong Spa 3 min), Benikea Daelim (→ Jungangno 4 min), Toyoko Daejeon (→ Gov. Complex Stn), Ramada Encore Cheonan (→ Bongmyeong 9 min), Brown Dot (→ 0.86 km/11 min), Skypark (→ Exit 9, 1–2 min).
- Policy fact-checks: **ibis Styles breakfast is ₩26,000, not free**; ibis Styles check-in 14:00 & laundry (paid) exists; Park Hyatt & L'Escape check-out 11:00; Nine Tree check-out 12:00.
- Rating corrections: ibis Styles Myeongdong listed 4★ on the official page (was 3); ibis Insadong listed 3★ (was 4).
- Four Seasons **Deluxe Room is one king bed** (was listed as queen).
- Duplicate promo lines de-duplicated; `_verification` notes added per record; `meta` updated (24 hotels, verification date, report pointer).

**Docs updated:** README (counts + verification note), `guide/cheonan.md` (shortlist now matches data; removed hotels documented), `guide/daejeon-vs-cheonan.md` (verdict note: Daejeon wins on shortlist depth), `guide/room-match.md` (official links fixed), `data/itinerary.json` (hotel counts; was also wrong for Daejeon — said 6, actually 7).

`validate.py` + `audit_report.py` pass: 24/24 published records pass the publication rules.

## 3. Remaining caveats (please read before booking)

1. **Bed width vs "queen":** Korean properties often sell a **140 cm "double"** as their base one-bed room. Official sources don't always publish widths (ibis Styles officially says "1 double bed"). For any room named *Double*, confirm the exact bed size on the booking engine; choose *Queen/King* room categories where offered. The "one bed, not two pushed together" rule **is** satisfied at all 24 kept hotels.
2. **Prices remain 2026 shoulder-season estimates** — re-check live rates on the official engine for Oct 31 – Nov 22 dates; the October foliage window sells out.
3. **Edge case:** LOTTE City Hotel Daejeon sits at the ~12–15 min boundary of the walk rule — verify the route in a map app before relying on it.
4. **With a taxi plan** (document per `guide/verification-checklist.md`), **Shilla Stay Cheonan** remains the best-quality Cheonan option, and **Sono Belle** is a genuine resort — they were only removed for the walk-to-station rule.
5. Small chains/motels (Brown Dot, Aank Air) have no working official booking site — OTA bookings with free cancellation are the safest route; verify policies in the OTA listing itself.

*Verified by automated official-page checks + authoritative listings on 2026-08-09. Next recheck advised 30–45 days before arrival (mid-September 2026).*
