import requests
import csv
import time

API_KEY = "5ae2e3f221c38a28845f05b61e162e10abf26414177bb9336af43455"

destinations = [
    {"destination_id": 1, "name": "Paris", "latitude": 48.8566, "longitude": 2.3522},
    {"destination_id": 2, "name": "Rome", "latitude": 41.9028, "longitude": 12.4964},
    {"destination_id": 3, "name": "Zurich", "latitude": 47.3769, "longitude": 8.5417},
]

def fetch_transport(lat, lon, radius=10000):
    url = "https://api.opentripmap.com/0.1/en/places/radius"
    params = {
        "apikey": API_KEY,
        "radius": radius,
        "lat": lat,
        "lon": lon,
        "kinds": "transport",
        "limit": 50,
        "rate": 2,                  # Show only well-rated items
        "format": "geojson"
    }
    r = requests.get(url, params=params)
    print(r.url)
    if r.status_code == 200:
        return r.json().get("features", [])
    else:
        print(f"❌ Error {r.status_code} fetching transport data")
        return []

transport_data = []

for dest in destinations:
    print(f"�� Fetching transport for {dest['name']}...")
    places = fetch_transport(dest["latitude"], dest["longitude"])

    for place in places:
        props = place.get("properties", {})
        geometry = place.get("geometry", {})

        transport_data.append({
            "destination_id": dest["destination_id"],
            "type": props.get("kinds", "").split(",")[0],
            "name": props.get("name", ""),
            "description": "",
            "start_location": "",  # Not available
            "end_location": "",    # Not available
            "price": "",           # Not available
            "duration_minutes": "",  # Not available
            "contact": "",         # Not available
            "latitude": geometry.get("coordinates", [0, 0])[1],
            "longitude": geometry.get("coordinates", [0, 0])[0],
        })

    time.sleep(1)  # Respect API rate limit

# Save to CSV
csv_file = "transport.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "destination_id", "type", "name", "description", "start_location", "end_location",
        "price", "duration_minutes", "contact", "latitude", "longitude"
    ])
    writer.writeheader()
    writer.writerows(transport_data)

print(f"✅ Saved {len(transport_data)} transport entries to {csv_file}")
