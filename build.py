#!/usr/bin/env python3
"""
Build script: generates index.html from the template + data files.

Why this exists (improvement #3 — "one source of truth"):
  - All hotel, itinerary, and trip data lives in data/*.json
  - index.template.html holds the HTML/JS shell with a __DATA__ placeholder
  - Running this script regenerates index.html so the embedded data never
    falls out of sync with the JSON files.

Usage:
    python3 build.py
"""
import json

HOTELS = 'data/hotels.json'
ITINERARY = 'data/itinerary.json'
TEMPLATE = 'index.template.html'
OUTPUT = 'index.html'


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main():
    hotels = load(HOTELS)
    itinerary = load(ITINERARY)

    data = {
        'trip': hotels['trip'],
        'split': hotels['split'],
        'itinerary': itinerary,
        'hotels': hotels['hotels'],
    }
    data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    with open(TEMPLATE, encoding='utf-8') as f:
        template = f.read()

    assert '__DATA__' in template, "placeholder __DATA__ missing in template"
    html = template.replace('__DATA__', data_json)

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Built {OUTPUT} ({len(html)} bytes) from {HOTELS} + {ITINERARY}")


if __name__ == '__main__':
    main()
