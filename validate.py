#!/usr/bin/env python3
"""
validate.py — Data quality checker for Korea-hotels

Checks hotels.json and itinerary.json for required fields and common issues.
Run with: python3 validate.py

2026-08-09 hardening (see RECOMMENDATIONS.md #2):
  - Field-type/contract checks (HTTPS official URLs, Korea geo bbox, price
    range sanity, currency whitelist, stationWalkTime format).
  - Transit-exception policy: the walk-to-station must-have may only be
    relaxed with an explicit `transitException: true` + documented
    `transitPlan` + `_verification` evidence. Bed/bathroom rules never relax.
  - Guard against the "planned leg with zero bookable hotels" gap: every
    itinerary leg city must have at least one published hotel (warning).
  - meta.totalHotels must match the actual record count.
"""

import json
import sys

HOTELS_FILE = "data/hotels.json"
ITINERARY_FILE = "data/itinerary.json"

REQUIRED_HOTEL_FIELDS = [
    "id", "city", "name", "tier", "stars", "area", "neighborhood",
    "priceFrom", "priceTo", "currency", "checkIn", "checkOut",
    "policies", "rooms", "promos", "amenities", "hasOnSiteLaundry",
    "officialLabel", "compareUrl", "compareLabel", "why", "highlights",
    "fits", "fitReason", "lat", "lng"
]

REQUIRED_ROOM_FIELDS = [
    "name", "price", "note", "bed", "bedType", "bedSize",
    "oneBed", "oneBedOnly", "privateBathroom", "bedNote"
]

ALLOWED_CURRENCIES = {"USD", "KRW"}
# South Korea rough bounding box (mainland + Jeju + Ulleungdo)
KOREA_LAT = (33.0, 39.5)
KOREA_LNG = (124.0, 132.5)
MAX_WALK_MINS = 15  # the walk-to-station must-have


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load {path}: {e}")
        sys.exit(1)


def validate_hotels(data):
    print("=== Validating hotels.json ===")
    hotels = data.get("hotels", [])
    print(f"Total hotels: {len(hotels)}")

    errors = 0
    warnings = 0
    cities_with_hotels = set()

    ids = [h.get('id') for h in hotels]
    names = [str(h.get('name', '')).strip().lower() for h in hotels]
    if len(ids) != len(set(ids)):
        print("  ❌ Duplicate hotel IDs found")
        errors += 1
    if len(names) != len(set(names)):
        print("  ❌ Duplicate hotel names found in curated shortlist")
        errors += 1

    for h in hotels:
        # Check required fields
        for field in REQUIRED_HOTEL_FIELDS:
            if field not in h:
                print(f"  ❌ Missing field '{field}' in {h.get('name', h.get('id'))}")
                errors += 1

        cities_with_hotels.add(h.get("city"))

        # Check rooms
        for room in h.get("rooms", []):
            for rfield in REQUIRED_ROOM_FIELDS:
                if rfield not in room:
                    print(f"  ❌ Missing room field '{rfield}' in {h['name']}")
                    errors += 1

        # Published shortlist policy: every hotel must pass all three must-haves.
        if h.get('fits') is not True:
            print(f"  ❌ {h['name']} does not pass the must-have requirements")
            errors += 1
        if not h.get("officialUrl"):
            print(f"  ❌ No officialUrl for {h['name']} (city: {h['city']})")
            errors += 1
        if not any(r.get('oneBedOnly') and r.get('privateBathroom') and r.get('bedType') in ('queen', 'king') for r in h.get('rooms', [])):
            print(f"  ❌ No qualifying single queen/king room for {h['name']}")
            errors += 1

        # Check hasOnSiteLaundry
        if "hasOnSiteLaundry" not in h:
            print(f"  ❌ Missing hasOnSiteLaundry in {h['name']}")
            errors += 1

        # --- Field-type / contract checks (2026-08-09 hardening) ---
        url = h.get("officialUrl") or ""
        if url and not url.startswith("https://"):
            print(f"  ❌ officialUrl for {h['name']} is not HTTPS: {url}")
            errors += 1

        lat, lng = h.get("lat"), h.get("lng")
        if not (isinstance(lat, (int, float)) and not isinstance(lat, bool) and KOREA_LAT[0] <= lat <= KOREA_LAT[1]):
            print(f"  ❌ lat out of South Korea range for {h['name']}: {lat}")
            errors += 1
        if not (isinstance(lng, (int, float)) and not isinstance(lng, bool) and KOREA_LNG[0] <= lng <= KOREA_LNG[1]):
            print(f"  ❌ lng out of South Korea range for {h['name']}: {lng}")
            errors += 1

        pf, pt = h.get("priceFrom"), h.get("priceTo")
        if not (isinstance(pf, int) and isinstance(pt, int) and not isinstance(pf, bool) and 0 < pf <= pt):
            print(f"  ❌ Bad price range for {h['name']}: {pf}–{pt}")
            errors += 1

        if h.get("currency") not in ALLOWED_CURRENCIES:
            print(f"  ❌ Unexpected currency for {h['name']}: {h.get('currency')}")
            errors += 1

        if not isinstance(h.get("stationWalkTime"), str):
            print(f"  ❌ stationWalkTime must be a string for {h['name']}")
            errors += 1

        # Transit-exception policy (2026-08-09): the walk-to-station must-have
        # may ONLY be relaxed with a documented plan. Bed/bathroom rules never relax.
        if h.get("transitException"):
            if not h.get("transitPlan"):
                print(f"  ❌ {h['name']} declares transitException without a transitPlan")
                errors += 1
            if not h.get("_verification"):
                print(f"  ❌ {h['name']} declares transitException without _verification evidence")
                errors += 1
            print(f"  ⚠️  {h['name']}: published under a documented transit exception")
            warnings += 1
        elif (h.get("_walkMins") or 0) > MAX_WALK_MINS:
            print(f"  ❌ {h['name']}: _walkMins {h['_walkMins']} exceeds the {MAX_WALK_MINS}-min walk rule without transitException")
            errors += 1

    # meta.totalHotels must match reality
    meta_total = data.get("meta", {}).get("totalHotels")
    if meta_total is not None and meta_total != len(hotels):
        print(f"  ❌ meta.totalHotels is {meta_total} but {len(hotels)} records are published")
        errors += 1

    if errors == 0:
        print("✅ No critical errors in hotels.json")
    else:
        print(f"❌ Found {errors} critical errors")

    if warnings > 0:
        print(f"⚠️  {warnings} warnings (documented transit exceptions)")

    return errors, cities_with_hotels


def validate_itinerary(data, cities_with_hotels):
    print("\n=== Validating itinerary.json ===")
    if "legs" not in data:
        print("❌ Missing 'legs' in itinerary.json")
        return 1

    legs = data["legs"]
    print(f"Legs: {len(legs)}")
    warnings = 0
    for leg in legs:
        city = leg.get("city")
        if city and city not in cities_with_hotels:
            print(f"  ⚠️  Planned leg '{city}' has NO published hotels — decision blocked for {leg.get('nights', '?')} nights")
            warnings += 1
    if warnings == 0:
        print("✅ Every planned leg has at least one published hotel")
    print("✅ itinerary.json looks valid")
    return 0  # zero-coverage legs are warnings, not hard failures


def main():
    print("🔍 Running Korea-hotels data validator...\n")

    hotels_data = load_json(HOTELS_FILE)
    itinerary_data = load_json(ITINERARY_FILE)

    hotel_errors, cities_with_hotels = validate_hotels(hotels_data)
    itinerary_errors = validate_itinerary(itinerary_data, cities_with_hotels)

    total_errors = hotel_errors + itinerary_errors

    print("\n=== Summary ===")
    if total_errors == 0:
        print("✅ All checks passed!")
    else:
        print(f"❌ {total_errors} issues found")

    sys.exit(total_errors)


if __name__ == "__main__":
    main()
