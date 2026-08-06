#!/usr/bin/env python3
"""
validate.py — Data quality checker for Korea-hotels

Checks hotels.json and itinerary.json for required fields and common issues.
Run with: python3 validate.py
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

    for h in hotels:
        # Check required fields
        for field in REQUIRED_HOTEL_FIELDS:
            if field not in h:
                print(f"  ❌ Missing field '{field}' in {h.get('name', h.get('id'))}")
                errors += 1

        # Check rooms
        for room in h.get("rooms", []):
            for rfield in REQUIRED_ROOM_FIELDS:
                if rfield not in room:
                    print(f"  ❌ Missing room field '{rfield}' in {h['name']}")
                    errors += 1

        # Check officialUrl
        if not h.get("officialUrl"):
            print(f"  ⚠️  No officialUrl for {h['name']} (city: {h['city']})")
            warnings += 1

        # Check hasOnSiteLaundry
        if "hasOnSiteLaundry" not in h:
            print(f"  ❌ Missing hasOnSiteLaundry in {h['name']}")
            errors += 1

    if errors == 0:
        print("✅ No critical errors in hotels.json")
    else:
        print(f"❌ Found {errors} critical errors")

    if warnings > 0:
        print(f"⚠️  {warnings} warnings (mostly missing officialUrl)")

    return errors

def validate_itinerary(data):
    print("\n=== Validating itinerary.json ===")
    if "legs" not in data:
        print("❌ Missing 'legs' in itinerary.json")
        return 1

    print(f"Legs: {len(data['legs'])}")
    print("✅ itinerary.json looks valid")
    return 0

def main():
    print("🔍 Running Korea-hotels data validator...\n")

    hotels_data = load_json(HOTELS_FILE)
    itinerary_data = load_json(ITINERARY_FILE)

    hotel_errors = validate_hotels(hotels_data)
    itinerary_errors = validate_itinerary(itinerary_data)

    total_errors = hotel_errors + itinerary_errors

    print("\n=== Summary ===")
    if total_errors == 0:
        print("✅ All checks passed!")
    else:
        print(f"❌ {total_errors} issues found")

    sys.exit(total_errors)

if __name__ == "__main__":
    main()
