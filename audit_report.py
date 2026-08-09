#!/usr/bin/env python3
"""Print a reproducible audit summary for the curated hotel shortlist."""
import json
from collections import Counter

with open('data/hotels.json', encoding='utf-8') as f:
    data=json.load(f)
hotels=data['hotels']
qualified=[]
for h in hotels:
    room=any(r.get('oneBedOnly') and r.get('privateBathroom') and r.get('bedType') in ('queen','king') for r in h.get('rooms',[]))
    qualified.append(bool(h.get('fits') and h.get('officialUrl') and room))
print('Published records:', len(hotels))
print('Unique IDs:', len({h['id'] for h in hotels}))
print('Unique names:', len({h['name'].strip().lower() for h in hotels}))
print('Pass all publication rules:', sum(qualified))
print('By city:', dict(Counter(h['city'] for h in hotels)))
print('Gyeongju approved:', sum(h['city']=='Gyeongju' for h in hotels))
assert len(hotels)==len(set(h['id'] for h in hotels))
assert all(qualified), 'A published hotel fails the publication rules'
