#!/usr/bin/env python3
"""
Apply the 2026-08-09 Gyeongju transit-exception pass (recommendation #1).

Adds two official-source-verified Gyeongju hotels to data/hotels.json under a
documented transit exception (Gyeongju has no subway; KTX arrives at Singyeongju,
~20 min from town), and records the two near-miss candidates in
data/excluded.json with re-add criteria. Bed and bathroom must-haves are NOT
relaxed.
"""
import json

HOTELS = 'data/hotels.json'
EXCLUDED = 'data/excluded.json'

TRANSIT_PLAN = (
    "KTX to Singyeongju Station (Gyeongju has no subway and no walk-to-rail option), "
    "then taxi ~20 min (approx ₩25,000–35,000) or tourist shuttle bus to the Bomun Lake "
    "resort complex. Bulguksa/Seokguram best reached by taxi, tour bus, or rental car."
)
STATION_TEXT = (
    "Transit exception: KTX Singyeongju Station ~20 min by taxi/shuttle "
    "(Gyeongju has no walk-to-station option)"
)

def queen_room(name, price, note, bed='queen', size="Queen (approx 150x200cm)"):
    return {
        "name": name,
        "price": price,
        "note": note,
        "bed": bed,
        "bedType": bed,
        "bedSize": size,
        "oneBed": True,
        "privateBathroom": True,
        "oneBedOnly": True,
        "bedNote": "Single %s bed (not two beds pushed together)" % bed,
    }

new_hotels = [
    {
        "id": "gyeongju-hilton",
        "city": "Gyeongju",
        "name": "Hilton Gyeongju",
        "tier": "premium",
        "stars": 5,
        "area": "Bomun Lake Resort (Gyeongju)",
        "neighborhood": "484-7 Bomun-ro, east shore of Bomun Lake in the Bomun Tourist Complex; ~6 km from the old-town tombs",
        "priceFrom": 125,
        "priceTo": 380,
        "currency": "USD",
        "checkIn": "15:00",
        "checkOut": "11:00",
        "policies": [
            "Check-in 15:00–23:59; check-out by 11:00 (per official Hilton page).",
            "Children over 1 year welcome; no cots/extra beds available.",
            "No pets.",
            "Indoor & seasonal outdoor pools, water slide, kids' areas."
        ],
        "rooms": [
            queen_room(
                "King Guest Room", "$125–140/night",
                "One king bed; resort or lake view; most standard category",
                bed='king', size="King (approx 180x200cm)"),
            queen_room(
                "Deluxe King", "$140–165/night",
                "Larger footprint, upgraded views",
                bed='king', size="King (approx 180x200cm)"),
        ],
        "promos": [
            "Hilton Honors: free sign-up for member rates + points; direct-booking perks.",
            "Official site (hilton.com) lists advance-purchase and stay-longer rates.",
            "Live official rates seen ~US$139+ for king rooms (2026 shoulder cross-check)."
        ],
        "amenities": [
            "Indoor pool",
            "Seasonal outdoor pool + water slide",
            "Fitness centre",
            "Multiple restaurants/bars",
            "Kids' areas",
            "Free Wi-Fi"
        ],
        "hasOnSiteLaundry": False,
        "officialUrl": "https://www.hilton.com/en/hotels/kyjgyhi-hilton-gyeongju/",
        "officialLabel": "Official site (hilton.com)",
        "compareUrl": "https://www.kayak.com/hotels/Gyeongju,c41830/Hilton-Gyeongju",
        "compareLabel": "Compare rates (KAYAK)",
        "why": "The quality pick for the Gyeongju leg: full 5★ resort on Bomun Lake with king-bed rooms — bookable on Hilton's official site with Honors member rates.",
        "highlights": [
            "Official Hilton booking with Honors points",
            "King-bed rooms (clearly meets one-bed rule)",
            "Lakeside resort facilities after sightseeing days"
        ],
        "fits": True,
        "fitReason": "King-bed rooms · transit exception: KTX Singyeongju ~20 min taxi/shuttle",
        "lat": 35.847,
        "lng": 129.281,
        "priceNote": "Typical 2026 estimates for king categories; autumn foliage weekends price high — check hilton.com for live rates.",
        "stationWalkTime": STATION_TEXT,
        "_walkMins": 20,
        "_bedSizes": ["king"],
        "hasCurrentDeal": False,
        "transitException": True,
        "transitPlan": TRANSIT_PLAN,
        "_verification": (
            "Official Hilton page (KYJGYHI) live and bookable, checked 2026-08-09; "
            "king-bed room categories confirmed by name on official site. Address 484-7 Bomun-ro "
            "cross-checked against OTA listings. TRANSIT EXCEPTION 2026-08-09: Gyeongju has no "
            "subway; KTX arrives at Singyeongju ~20 min from Bomun Lake — taxi/shuttle plan "
            "documented in transitPlan."
        ),
    },
    {
        "id": "gyeongju-lahan-select",
        "city": "Gyeongju",
        "name": "Lahan Select Gyeongju",
        "tier": "premium",
        "stars": 5,
        "area": "Bomun Lake Resort (Gyeongju)",
        "neighborhood": "338 Bomun-ro, south shore of Bomun Lake; 745-room resort with full spa",
        "priceFrom": 100,
        "priceTo": 150,
        "currency": "USD",
        "checkIn": "15:00",
        "checkOut": "11:00",
        "policies": [
            "Check-in from 15:00; check-out by 11:00.",
            "Indoor & outdoor pools, full spa and sauna.",
            "Large resort (745 rooms) — still sells out for autumn foliage weekends.",
            "No pets."
        ],
        "rooms": [
            {
                "name": "Queen Room",
                "price": "$120–150/night",
                "note": "One queen bed; mountain or lake view; confirm the ONE-bed queen category at booking (the hotel also sells 2-queen lake rooms)",
                "bed": "queen",
                "bedType": "queen",
                "bedSize": "Queen (approx 150cm+; official room type 'Queen')",
                "oneBed": True,
                "privateBathroom": True,
                "oneBedOnly": True,
                "bedNote": "One queen bed unit (not two beds pushed together); avoid the '2 Queen Beds' lake room",
            },
            {
                "name": "Deluxe Double",
                "price": "$100–120/night",
                "note": "37 m², one double bed; pool-access packages common — narrower than the Queen category",
                "bed": "double",
                "bedType": "double",
                "bedSize": "Double (approx 140cm — below our 150cm queen minimum; shown for completeness)",
                "oneBed": True,
                "privateBathroom": True,
                "oneBedOnly": True,
                "bedNote": "One double bed (~140cm). Fails our queen-width rule — choose the Queen Room instead.",
            },
        ],
        "promos": [
            "Official site (lahan.com) runs seasonal lake-view and length-of-stay packages.",
            "Pool-access room packages for 2 adults appear regularly on the official booking engine.",
            "OTA cross-check 2026-08-09: deluxe doubles ~US$100–130, lake rooms ~US$150+."
        ],
        "amenities": [
            "Indoor & outdoor pools",
            "Full spa & sauna",
            "Balcony rooms (most categories)",
            "Restaurants & bar",
            "Free Wi-Fi"
        ],
        "hasOnSiteLaundry": False,
        "officialUrl": "https://www.lahan.com/gyeongju/en/main.do",
        "officialLabel": "Official site (lahan.com)",
        "compareUrl": "https://www.kayak.com/hotels/Gyeongju,c41830/Lahan-Select-Gyeongju",
        "compareLabel": "Compare rates (KAYAK)",
        "why": "Big lakeside resort with a clear single-queen category and frequent official-site packages — usually cheaper than Hilton for similar facilities.",
        "highlights": [
            "One-queen room category (confirm at booking)",
            "Full spa + indoor/outdoor pools",
            "Official packages on lahan.com"
        ],
        "fits": True,
        "fitReason": "One-queen room category · transit exception: KTX Singyeongju ~20 min taxi/shuttle",
        "lat": 35.840,
        "lng": 129.291,
        "priceNote": "Typical 2026 estimates; foliage-season weekends run higher. Check lahan.com for live package rates.",
        "stationWalkTime": STATION_TEXT,
        "_walkMins": 20,
        "_bedSizes": ["queen", "double"],
        "hasCurrentDeal": False,
        "transitException": True,
        "transitPlan": TRANSIT_PLAN,
        "_verification": (
            "Official domain lahan.com/gyeongju confirmed as the Lahan Hotels chain's Gyeongju "
            "page (checked 2026-08-09); address 338 Bomun-ro cross-checked via VISITKOREA/OTA "
            "listings. 'Queen' one-bed room type per official research (guide/gyeongju.md); "
            "OTA listings also show 2-queen rooms — record instructs to book the one-bed category. "
            "TRANSIT EXCEPTION 2026-08-09: no subway in Gyeongju; KTX Singyeongju ~20 min out — "
            "taxi/shuttle plan documented."
        ),
    },
]

excluded_additions = [
    {
        "id": "gyeongju-commodore",
        "city": "Gyeongju",
        "name": "Commodore Hotel Gyeongju",
        "tier": "mid",
        "stars": 4,
        "area": "Bomun Lake Resort (Gyeongju)",
        "neighborhood": "422 Bomun-ro, Bomun Tourist Complex; lakeside, ~6 km from old-town sights",
        "priceFrom": 66,
        "priceTo": 130,
        "currency": "USD",
        "checkIn": "15:00",
        "checkOut": "11:00",
        "policies": [
            "OTA listings differ on exact times (14:00–15:00 check-in, 11:00–12:00 check-out) — confirm on official site.",
            "Free Wi-Fi; sauna and seasonal outdoor pool; 3 restaurants.",
            "No pets."
        ],
        "rooms": [
            {
                "name": "Superior Double (Mountain View)",
                "price": "$66–80/night",
                "note": "28–30 m²; private bath (bath + shower)",
                "bed": "double",
                "bedType": "double",
                "bedSize": "1 double bed — OTAs list 'full' (~140cm); some property descriptions say 'king-size' — UNCONFIRMED",
                "oneBed": True,
                "privateBathroom": True,
                "oneBedOnly": True,
                "bedNote": "One bed unit, but width unconfirmed (140cm 'full' vs king-size claims)",
            },
            {
                "name": "Superior Double (Lake View)",
                "price": "$100–130/night",
                "note": "30 m², Bomun Lake view; private bath",
                "bed": "double",
                "bedType": "double",
                "bedSize": "1 double bed — width UNCONFIRMED (sources differ)",
                "oneBed": True,
                "privateBathroom": True,
                "oneBedOnly": True,
                "bedNote": "One bed unit, but width unconfirmed (140cm 'full' vs king-size claims)",
            },
        ],
        "promos": ["Official site runs seasonal lake-view packages (per guide/gyeongju.md)."],
        "amenities": ["Sauna", "Seasonal outdoor pool", "3 restaurants", "Business center", "Convenience store", "Free Wi-Fi", "Free parking"],
        "hasOnSiteLaundry": False,
        "officialUrl": "https://www.commodorehotel.co.kr",
        "officialLabel": "Official site (commodorehotel.co.kr)",
        "compareUrl": "https://www.kayak.com/hotels/Gyeongju,c41830/Commodore-Hotel-Gyeongju",
        "compareLabel": "Compare rates (KAYAK)",
        "why": "Best mid-price candidate at Bomun Lake — official site and VISITKOREA listing fully verified; withheld pending bed-width confirmation.",
        "highlights": ["VISITKOREA-verified official source", "Private bathrooms confirmed", "Mid-tier pricing $66–130"],
        "fits": False,
        "fitReason": "Fails one-queen/king rule pending official bed-width confirmation; also transit exception",
        "lat": 35.844,
        "lng": 129.285,
        "priceNote": "Typical 2026 estimates (guide/gyeongju.md + OTA cross-check 2026-08-09).",
        "stationWalkTime": STATION_TEXT,
        "_walkMins": 20,
        "_bedSizes": ["double"],
        "hasCurrentDeal": False,
        "excludedOn": "2026-08-09",
        "exclusionReasons": [
            "BED RULE (non-negotiable): one-bed rooms listed as '1 double bed (full)' (~140cm) on OTAs; marketing text claims 'double bed or king-size bed' — no official confirmation of a queen/king (>=150cm) one-bed room yet.",
            "TRANSIT: no walk-to-station option (KTX Singyeongju ~20 min taxi) — acceptable only under the documented transit-exception policy."
        ],
        "verificationEvidence": (
            "Existence/address (422 Bomun-ro), official website (commodorehotel.co.kr) and 4-star "
            "class confirmed via VISITKOREA official listing (vcontsId 99034, geo 35.8442/129.2851), "
            "checked 2026-08-09. Private en-suite bathrooms confirmed across room types (OTA room "
            "descriptions). Bed width unresolved: Booking.com lists '1 full bed' for Superior Double; "
            "easemytrip states rooms have 'a double bed or a king-size bed'."
        ),
        "verificationNote": (
            "RE-ADD CRITERIA: publish (with transitException) once the official booking engine or "
            "the hotel confirms a one-bed queen/king room category. Everything else already verifies."
        ),
    },
    {
        "id": "gyeongju-gg-hotel",
        "city": "Gyeongju",
        "name": "GG Hotel Gyeongju",
        "tier": "budget",
        "stars": 3,
        "area": "Gyeongju Old Town edge",
        "neighborhood": "Taejong-ro 699beon-gil 3, south edge of the historic centre; walkable to tombs/Cheomseongdae area",
        "priceFrom": 55,
        "priceTo": 82,
        "currency": "USD",
        "checkIn": "15:00",
        "checkOut": "11:00",
        "policies": ["Times per OTA listings (no official English site to confirm)."],
        "rooms": [
            {
                "name": "Standard Double Room",
                "price": "$55–66/night",
                "note": "1 double bed (per OTA listings); private bathroom",
                "bed": "double",
                "bedType": "double",
                "bedSize": "Double (~140cm; width unconfirmed by any official source)",
                "oneBed": True,
                "privateBathroom": True,
                "oneBedOnly": True,
                "bedNote": "One double bed (OTA evidence only)",
            }
        ],
        "promos": [],
        "amenities": ["Free Wi-Fi (per OTA listings)"],
        "hasOnSiteLaundry": False,
        "officialUrl": None,
        "officialLabel": "No official English site",
        "compareUrl": "https://www.kayak.com/hotels/Gyeongju,c41830/GG-Hotel-Gyeongju",
        "compareLabel": "Compare rates (KAYAK)",
        "why": "Only budget candidate in Gyeongju — withheld because no official booking source exists.",
        "highlights": ["Budget pricing $55–82", "Old-town location"],
        "fits": False,
        "fitReason": "Fails official-source rule (OTA-only) + bed width unconfirmed + transit exception",
        "lat": 35.989,
        "lng": 129.215,
        "priceNote": "OTA-observed 2026 pricing ($56–82); cannot verify against an official channel.",
        "stationWalkTime": STATION_TEXT,
        "_walkMins": 20,
        "_bedSizes": ["double"],
        "hasCurrentDeal": False,
        "excludedOn": "2026-08-09",
        "exclusionReasons": [
            "OFFICIAL-SOURCE RULE: no official English website or chain page — every published record must be verifiable against an official source (OTA-only listings are cross-check tools, not sources).",
            "BED RULE: '1 double bed' per OTAs; width (~140cm) below the 150cm queen minimum with no official confirmation.",
            "TRANSIT: no walk-to-station option."
        ],
        "verificationEvidence": (
            "Real operating property per KAYAK/Trip.com/Google Hotels listings (Standard Double "
            "~US$56–70, 1 double bed), checked 2026-08-09. No official site found; not listed on "
            "VISITKOREA at time of check."
        ),
        "verificationNote": (
            "RE-ADD CRITERIA: an official/VISITKOREA listing plus a confirmed queen-or-larger one-bed "
            "room, under the transit-exception policy."
        ),
    },
]


def main():
    with open(HOTELS, encoding='utf-8') as f:
        hotels_data = json.load(f)
    with open(EXCLUDED, encoding='utf-8') as f:
        excluded_data = json.load(f)

    existing_ids = {h['id'] for h in hotels_data['hotels']}
    for h in new_hotels:
        assert h['id'] not in existing_ids, f"{h['id']} already published"
        hotels_data['hotels'].append(h)

    existing_excl = {h['id'] for h in excluded_data['excludedHotels']}
    for h in excluded_additions:
        assert h['id'] not in existing_excl and h['id'] not in existing_ids
        excluded_data['excludedHotels'].append(h)

    meta = hotels_data['meta']
    meta['totalHotels'] = len(hotels_data['hotels'])
    meta['lastUpdated'] = '2026-08-09'
    meta['gyeongjuTransitException'] = (
        "2026-08-09: 2 Gyeongju hotels (Hilton Gyeongju, Lahan Select Gyeongju) published "
        "under the documented transit-exception policy (transitException + transitPlan). "
        "Bed & bathroom must-haves unchanged; Commodore Hotel Gyeongju and GG Hotel "
        "Gyeongju moved to data/excluded.json pending bed-width/official-source confirmation."
    )
    excluded_data['lastUpdated'] = '2026-08-09'

    with open(HOTELS, 'w', encoding='utf-8') as f:
        json.dump(hotels_data, f, ensure_ascii=False, indent=1)
        f.write('\n')
    with open(EXCLUDED, 'w', encoding='utf-8') as f:
        json.dump(excluded_data, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(f"hotels.json now {meta['totalHotels']} records; excluded.json now "
          f"{len(excluded_data['excludedHotels'])} records")


if __name__ == '__main__':
    main()
