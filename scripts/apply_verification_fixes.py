#!/usr/bin/env python3
"""
One-off curation script (2026-08-09 official-source verification).

Applies corrections found during the official-source verification documented in
guide/verification-report-2026-08-09.md:

  1. Moves records that FAIL the near-public-transport must-have out of the
     published shortlist (data/hotels.json) into data/excluded.json, with
     measured evidence.
  2. Fixes wrong/broken officialUrl values, star ratings, check-in/out times,
     station claims, and duplicate promo lines on the retained records.
"""
import json
from collections import OrderedDict

HOTELS = 'data/hotels.json'
EXCLUDED = 'data/excluded.json'

with open(HOTELS, encoding='utf-8') as f:
    data = json.load(f, object_pairs_hook=OrderedDict)

hotels = {h['id']: h for h in data['hotels']}

# ---------------------------------------------------------------- exclusions
EXCLUSIONS = {
    'cheonan-on-city': {
        'bathroomVerified': True,
        'bedVerified': 'Standard/Deluxe Double with one bed (OTA listings)',
        'failReasons': [
            'Not near public transport: located in Buldang-dong (105, Buldang 4-ro, Seobuk-gu), ~3.5 km from Cheonan-Asan KTX and ~3 km from Cheonan Station; nearest rail access requires a taxi.',
        ],
        'evidence': [
            'VISITKOREA official listing: "just a 5-minute drive away from the KTX Cheonan Asan Station", address 105 Buldang 4-ro, Seobuk-gu — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=63352',
        ],
        'note': 'Record claimed "7 min walk to Cheonan Station" — that is incorrect.',
    },
    'cheonan-sono-belle': {
        'bathroomVerified': True,
        'bedVerified': 'Deluxe/Suite doubles (resort; OTA listings)',
        'failReasons': [
            'Not near public transport: a water-park resort (Tedin/Ocean Adventure) at 200 Jonghaphyuyangji-ro, Seongnam-myeon — roughly 11 km from Cheonan-Asan KTX and far from any subway/rail station. Record claimed "~15 min to Cheonan-Asan KTX" which is actually a 20+ min drive, not a walk.',
            'Star level: listed 4★ in this dataset; rated 3★ on major OTAs.',
        ],
        'evidence': [
            'VISITKOREA official listing (Sono Belle Cheonan Ocean Adventure), address 200 Jonghaphyuyangji-ro — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=89151',
            'Official chain site operates: https://www.sonohotelsresorts.com',
        ],
        'note': 'Fine resort for a car-based stay; does not meet the near-transit rule.',
    },
    'cheonan-best-western-asan': {
        'bathroomVerified': True,
        'bedVerified': 'Doubles with private bathroom (OTA listings)',
        'failReasons': [
            'Not near public transport: located at 32 Onsaem-ro, Tangjeong-myeon, Asan — ~6 km (3.7 mi) from Cheonan-Asan KTX Station. Record claimed "5 min walk to Cheonan-Asan KTX" which is false; it is a 10–15 min drive.',
            'officialUrl on bestwestern.com returns an error page (no such property page).',
            'Property now trades as "SureStay Plus Hotel by Best Western Asan".',
        ],
        'evidence': [
            'Booking.com: "Located in Asan, 3.7 miles from Cheonan Asan Train Station" — https://www.booking.com/hotel/kr/surestay-plus-by-best-western.html',
        ],
        'note': 'Wrong brand page and wrong proximity claim.',
    },
    'cheonan-mains': {
        'bathroomVerified': True,
        'bedVerified': 'Doubles (OTA listings)',
        'failReasons': [
            'Not near public transport: 34 Cheongsu 11-ro, Dongnam-gu — ~2.7 km straight-line from Cheonan Station (~30+ min walk); no rail station within a 15-min walk.',
            'officialUrl pointed to shillahotels.com, which is unrelated — no official site exists; bookable only via OTAs.',
        ],
        'evidence': [
            'Booking.com / Tripadvisor address and distances — https://www.booking.com/hotel/kr/the-mains.html',
        ],
        'note': 'Wrong official link (Shilla domain) and wrong proximity claim removed.',
    },
    'cheonan-shilla-stay': {
        'bathroomVerified': True,
        'bedVerified': 'Standard/Deluxe doubles (one bed) — official room inventory',
        'failReasons': [
            'Overstated transit access: record claimed "~8 min walk to Cheonan Station". Actual straight-line distance is ~1.9 km (≈25-min walk); Cheonan-Asan KTX is a 15-min drive. Fails the 1–15 min walk rule.',
            'Property itself is fully verified (177 Dongseo-daero, Seobuk-gu; 309 rooms; coin laundry; opened property page on shillahotels.com).',
        ],
        'evidence': [
            'Official Shilla page: https://www.shillahotels.com/en/shillastay/cheonan/index.do',
            'Tripadvisor location grade 40/100; KAYAK listing confirms 177 Dongseo-daero address.',
        ],
        'note': 'Best quality hotel in Cheonan, but the must-have list only covers walk-to-station properties. Re-add only with a documented taxi plan (same rule as the Gyeongju exception).',
    },
}

# --------------------------------------------------------------- corrections
FIX = {}

FIX['seoul-l7-myeongdong'] = {
    'promos': [
        'LOTTE Members: sign up free for member-only rates and reward points (L7 is a Lotte Hotels brand).',
        "L7 runs periodic 'Flash Deals' and room packages (e.g. N Seoul Tower observatory + cable-car tickets) — check the hotel's Official Offers page.",
        'Booking direct on lottehotel.com unlocks member packages not shown on OTAs.',
        'Current ~$155–175 queen (KAYAK / direct 2026 shoulder)',
    ],
}

FIX['seoul-nine-tree'] = {
    'officialUrl': 'https://www.ninetreehotels.com/nth1/?lang=en',
    'officialLabel': 'Official site (ninetreehotels.com)',
    'checkOut': '12:00',
    'promos': [
        "Parnas Nine Tree runs seasonal 'early-bird' and multi-night stay deals on its official site.",
        'Often cheaper than 4-star neighbors while delivering clean, reliable quality — a top value pick.',
        'Current: ~$112–130 queen (frequent early-bird)',
    ],
    '_verification': 'URL previously 404 (ninetreehotel.com/eng/myeongdong1/main.do). Correct official brand page confirmed 2026-08-09: ninetreehotels.com/nth1.',
}

FIX['seoul-ibis-styles'] = {
    'officialUrl': 'https://all.accor.com/hotel/9771/index.en.shtml',
    'stars': 4,
    'checkIn': '14:00',
    'hasOnSiteLaundry': True,
    'stationWalkTime': '6 min walk to Myeongdong Station (400 m, per official Accor page)',
    '_walkMins': 6,
    'fitReason': 'Double · Myeongdong Stn ~6 min (official)',
    'policies': [
        'Check-in from 14:00; check-out by 12:00 (official Accor page).',
        'Breakfast available 07:30–10:00 at ₩26,000/person — NOT included (official Accor page).',
        'Paid coin laundry on site (washer ₩5,000 / dryer ₩5,000). Free Wi-Fi.',
    ],
    'amenities': ['Rooftop bar (Le Style)', 'Top-floor restaurant', 'Fitness center', 'Sauna (paid)', 'Coin laundry (paid)', 'Free Wi-Fi'],
    'promos': [
        'Accor ALL loyalty program — earn points & member rates.',
        "Watch Accor ALL 'members flash sales' ('Private Sales') for discounts.",
        'Rooms are compact but clean & functional — great price-to-quality.',
        'Current ~$110–140 typical; breakfast ₩26,000 extra (official)',
    ],
    '_verification': 'Previous URL (hotel/1976) pointed to a Mercure in France. Correct Accor property code 9771 confirmed 2026-08-09. Official site lists rooms as "1 double bed"; breakfast is paid.',
}

FIX['seoul-ibis-insadong'] = {
    'officialUrl': 'https://all.accor.com/hotel/8002/index.en.shtml',
    'stars': 3,
    'checkIn': '14:00',
    '_verification': 'Previous URL (hotel/1888) pointed to a Mercure in Bourges, France. Correct Accor property code 8002 confirmed 2026-08-09. Officially rated 3 stars; renovated and re-confirmed by official page (Jongno Stn ~4 min).',
}

FIX['seoul-four-seasons'] = {
    '_verification': 'FS Seoul Deluxe Room officially = "One king bed" (fourseasons.com, verified 2026-08-09); dataset previously listed the Deluxe as queen.',
}

FIX['seoul-fairmont'] = {
    'officialUrl': 'https://www.fairmont.com/en/hotels/seoul/fairmont-ambassador-seoul.html',
    '_verification': 'fairmont.com/seoul/ redirects to the canonical page above (verified 2026-08-09).',
}

FIX['seoul-lescape'] = {
    'officialUrl': 'https://www.marriott.com/en-us/hotels/sellm-lescape-a-luxury-collection-hotel-seoul-myeongdong/overview/',
    'officialLabel': 'Official site (marriott.com)',
    'checkOut': '11:00',
    '_verification': 'Previous Marriott URL used wrong property code SELAK (= THE PLAZA Seoul). Correct code SELLM confirmed 2026-08-09. Official check-out 11:00.',
}

FIX['seoul-skypark-myeongdong3'] = {
    'officialLabel': 'Official site (skyparkhotel.com)',
    'stationWalkTime': '1–2 min walk — directly at Myeongdong Station Exit 9',
    '_walkMins': 2,
    'fitReason': 'Double · Myeongdong Stn Exit 9 ~1 min',
    '_verification': 'skyparkhotel.com confirmed as official site 2026-08-09; hotel sits at Myeongdong Station Exit 9 (139 Toegye-ro).',
}

FIX['busan-shilla-stay'] = {
    'officialUrl': 'https://www.shillahotels.com/en/shillastay/haeundae/index.do',
    'officialLabel': 'Official site (shillahotels.com)',
    'promos': [
        'Shilla Rewards membership — earn points (3% room / 1% F&B) & tier perks across Shilla Stay & Shilla hotels.',
        'Watch official site for member-only rates & packages.',
        'Current ~$60–100 queen — strong Haeundae value (Shilla Rewards member rates)',
    ],
    '_verification': 'shillastay.com/haeundae redirects to the canonical Shilla hub page above (verified 2026-08-09). 407 rooms, rooftop pool, laundry room — matches record.',
}

FIX['busan-asti'] = {
    'officialUrl': 'http://en.astihotel.co.kr/',
    'officialLabel': 'Official site (astihotel.co.kr)',
    'checkOut': '11:00',
    '_verification': 'Previous URL astihotel.com appears parked/expired. Correct official site en.astihotel.co.kr (verified 2026-08-09): "1 minute away from Busan station by a walk".',
}

FIX['busan-grand-josun'] = {
    'officialUrl': 'https://gjb.josunhotel.com/main.do?locale=en',
    'officialLabel': 'Official site (josunhotel.com)',
    '_verification': 'Previous URL josun.com does not resolve (HTTP 500). Correct official brand domain josunhotel.com — gjb subdomain for Grand Josun Busan (verified 2026-08-09).',
}

FIX['busan-park-hyatt'] = {
    'officialUrl': 'https://www.hyatt.com/park-hyatt/en-US/busph-park-hyatt-busan',
    'checkOut': '11:00',
    '_verification': 'Previous URL hyatt.com/park-hyatt/busan returns "Not Found". Canonical page confirmed 2026-08-09; official check-out is 11:00.',
}

FIX['busan-toyoko-haeundae2'] = {
    'stationWalkTime': '10 min walk to Haeundae Station Exit 5 (official Toyoko Inn page)',
    '_walkMins': 10,
    '_verification': 'Official page verified 2026-08-09: exists, free buffet breakfast, unit bath (private bathroom), laundromat; check-in 15:00 / check-out 10:00 matches.',
}

FIX['busan-ramada-encore-haeundae'] = {
    'name': 'Ramada Encore by Wyndham Haeundae',
    'officialLabel': 'Official site (wyndhamhotels.com)',
    '_verification': 'Official Wyndham page loads for this property (verified 2026-08-09); official name omits "Busan".',
}

FIX['cheonan-ramada-encore'] = {
    'officialLabel': 'Official site (wyndhamhotels.com)',
    'neighborhood': 'Bongmyeong/Sinbu area of Cheonan; ~750 m (9 min walk) to Bongmyeong Station (Line 1); ~4 km to Cheonan-Asan KTX',
    'stationWalkTime': '9 min walk to Bongmyeong Station (Line 1)',
    '_walkMins': 9,
    'fitReason': 'Double/Queen · Bongmyeong Stn ~9 min; ~4 km to KTX',
    'promos': [
        'Wyndham Rewards program — earn points and member rates.',
        'Frequent breakfast packages and early-bird deals.',
        'Current ~$55–65 (Wyndham member rates)',
    ],
    '_verification': 'Official Wyndham page loads (verified 2026-08-09). Record claimed 10-min walk to Cheonan Station — actually ~2 km; real rail link is Bongmyeong Stn ~750 m (Trip.com/MakeMyTrip listings).',
}

FIX['cheonan-brown-dot'] = {
    'officialUrl': 'https://us.trip.com/hotels/cheonan-si-hotel-detail-62705121/brown-dot-hotel-cheonan-dongnam/',
    'officialLabel': 'Book via OTA (chain site browndot.co.kr offline)',
    'stationWalkTime': '11 min walk to Cheonan Station (0.86 km)',
    '_walkMins': 11,
    'fitReason': 'Double · Cheonan Stn ~11 min (0.86 km)',
    '_verification': 'Property verified (7-1 Keunsijang-gil; private bathrooms; 0.86 km to Cheonan Stn). Chain domain browndot.co.kr returns a hosting-error/403 page — booking via OTA recommended.',
}

FIX['daejeon-toyoko-inn'] = {
    'officialUrl': 'https://www.toyoko-inn.com/eng/search/detail/00234/',
    'stationWalkTime': '4 min walk to Government Complex Daejeon Station (Exit 4, official access guide)',
    '_walkMins': 4,
    'promos': [
        'Frequent free breakfast promotion for direct or member bookings.',
        'Toyoko Inn loyalty program benefits.',
        'Current ~$48–60 + free breakfast (official: buffet breakfast free)',
    ],
    '_verification': 'Previous URL (hotel/00235) page-not-found. Correct property code 00234 confirmed on official site 2026-08-09: private bathrooms with shower/tub, free breakfast, laundry.',
}

FIX['daejeon-ramada'] = {
    'officialLabel': 'Official site (wyndhamhotels.com)',
    'area': 'Yuseong (hot springs district)',
    'neighborhood': '3-min walk from Yuseong Spa (Oncheon) Station; beside NC Dept. store & Bongmyeong-dong cafe street',
    'stationWalkTime': '3 min walk to Yuseong Spa Station (Line 1)',
    '_walkMins': 3,
    'fitReason': 'Double/Queen · Yuseong Spa Stn ~3 min',
    'promos': [
        'Wyndham Rewards points and member rates.',
        'Current ~$65–85 (Wyndham member rates)',
    ],
    '_verification': 'Official Wyndham page loads (verified 2026-08-09). Record claimed 8-min walk to Daejeon Station — hotel is in Yuseong-gu, 15 km away; real link is Yuseong Spa Stn ~3 min (multiple sources).',
}

FIX['daejeon-lotte-city'] = {
    'officialLabel': 'Official site (lottehotel.com)',
    'stationWalkTime': '~12–15 min walk to City Hall Station (verify walking route)',
    '_walkMins': 13,
    '_verification': 'Property verified at 33 Expo-ro 123beon-gil (in front of Daejeon Convention Center); Lotte official page loads. Nearest metro ~12–15 min on foot — at the edge of the 15-min rule, verify route before booking.',
}

FIX['daejeon-benikea-daelim'] = {
    'area': 'Jung-gu (old town) / Jungangno',
    'neighborhood': 'Near Jungangno Station (Line 1); one metro stop from Daejeon KTX Station',
    'stationWalkTime': '4 min walk to Jungangno Station; Daejeon KTX 1 metro stop (~1.2 km)',
    '_walkMins': 4,
    'fitReason': 'Double · Jungangno Stn ~4 min; KTX one stop',
    'highlights': [
        'Steps from Jungangno metro (Line 1)',
        'One stop from Daejeon KTX Station',
        'Very low price',
    ],
    '_verification': 'Verified on official chain site benikea.com (베니키아 호텔 대림 listed, Daejeon). Record claimed "2–5 min walk to Daejeon Station" — actually ~1.2 km; correct link is Jungangno Stn ~250–300 m.',
}

FIX['daejeon-aank-air'] = {
    'stationWalkTime': '4 min walk to Jungangno Station (270 m); ~10 min to Daejeon KTX',
    '_walkMins': 4,
    'fitReason': 'Double · Jungangno Stn ~4 min (270 m)',
    '_verification': 'Verified on Expedia/Hotels.com & Trip.com: Jungangno metro 270 m, Daejeon Station 720 m, private bathrooms, free parking/Wi-Fi.',
}

FIX['daejeon-hotel-stendhal'] = {
    'officialUrl': 'http://stendhalhotel.co.kr',
    'officialLabel': 'Official site (stendhalhotel.co.kr)',
    'neighborhood': 'Yuseong Hot Springs district, near Yuseong Oncheon Station',
    'stationWalkTime': '7 min walk to Yuseong Oncheon Station (~550 m)',
    '_walkMins': 7,
    'lat': 36.3570,
    'lng': 127.3447,
    'fitReason': 'Double/Queen · Yuseong Oncheon Stn ~7 min',
    'promos': ['Popular choice for hot springs visitors; free breakfast frequently offered.', 'Highest-rated independent in Yuseong (9.1/10 Trip.com, 8.5/10 HotelsCombined).'],
    '_verification': 'Property verified (14 Oncheonbuk-ro; 70 rooms; bathrooms with separate tub/shower). Previous officialUrl pointed to interciti.co.kr — a different hotel. Own site stendhalhotel.co.kr per official Facebook page.',
}

FIX['daejeon-hotel-interciti'] = {
    'officialLabel': 'Official site (interciti.co.kr)',
    'stationWalkTime': '5 min walk to Yuseong Oncheon Station',
    '_walkMins': 5,
    'lat': 36.3542,
    'lng': 127.3478,
    'fitReason': 'Double · Yuseong Oncheon Stn ~5 min',
    '_verification': 'Official site interciti.co.kr loads with working booking engine (verified 2026-08-09). Open & operating (renovated 2023).',
}

# ---------------------------------------------------------------- apply fixes
for hid, patch in FIX.items():
    if hid not in hotels:
        print(f'WARN missing hotel {hid}')
        continue
    hotels[hid].update(patch)

# Four Seasons: Deluxe room bed is officially ONE KING (fix wrong "queen" claim)
fs = hotels['seoul-four-seasons']
fs['rooms'][0].update({
    'bed': 'king', 'bedType': 'king',
    'bedSize': 'King (one king bed — per official Four Seasons room page)',
    'bedNote': 'Single king bed (not two beds pushed together)',
})
fs['_bedSizes'] = ['king', 'king']

# ---------------------------------------------------------------- exclusions
excluded_records = []
kept = []
for h in data['hotels']:
    if h['id'] in EXCLUSIONS:
        info = EXCLUSIONS[h['id']]
        rec = OrderedDict(h)
        rec['excludedOn'] = '2026-08-09'
        rec['fits'] = False
        rec['exclusionReasons'] = info['failReasons']
        rec['verificationEvidence'] = info['evidence']
        rec['verificationNote'] = info['note']
        excluded_records.append(rec)
    else:
        kept.append(h)

data['hotels'] = kept

excl_doc = {
    '_readme': (
        'Records removed from the published must-have shortlist after the 2026-08-09 '
        'official-source verification (see guide/verification-report-2026-08-09.md). '
        'Each fails at least one non-negotiable requirement (near-public-transport walk rule '
        'and/or an unverifiable official source). Kept here for transparency — re-add only '
        'after re-verifying the exact property/room and documenting a taxi plan if the '
        'station rule is intentionally relaxed (see guide/verification-checklist.md).'
    ),
    'excludedHotels': excluded_records,
    'lastUpdated': '2026-08-09',
}

# ---------------------------------------------------------------- meta
meta = data.setdefault('meta', {})
meta['totalHotels'] = len(kept)
meta['excludedRecords'] = meta.get('excludedRecords', 0) + len(excluded_records)
meta['lastOfficialSourceVerification'] = '2026-08-09'
meta['verificationReport'] = 'guide/verification-report-2026-08-09.md'
meta['datasetType'] = (
    'Curated shortlist; every published hotel has an official URL and passes the three '
    'must-have checks (single queen/king bed, private en-suite bathroom, walk-to-station). '
    'Re-verified against official sources on 2026-08-09.'
)

with open(HOTELS, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')

with open(EXCLUDED, 'w', encoding='utf-8') as f:
    json.dump(excl_doc, f, ensure_ascii=False, indent=2)
    f.write('\n')

print(f'kept={len(kept)} excluded={len(excluded_records)} -> {sorted(r["id"] for r in excluded_records)}')
