import requests
import csv
import time

API_KEY = "5ae2e3f221c38a28845f05b61e162e10abf26414177bb9336af43455"

# Define destinations and their destination_id from your DB
destinations = [
    {"destination_id": 1, "name": "Paris", "lat": 48.8566, "lon": 2.3522},
    {"destination_id": 2, "name": "Rome", "lat": 41.9028, "lon": 12.4964},
    {"destination_id": 3, "name": "Zurich", "lat": 47.3769, "lon": 8.5417}
]

# Function to get nearby places (e.g., parks, museums)
def get_places(lat, lon, radius=3000, kinds="interesting_places", limit=10):
    url = "https://api.opentripmap.com/0.1/en/places/radius"
    params = {
        "apikey": API_KEY,
        "radius": radius,
        "lon": lon,
        "lat": lat,
        "kinds": kinds,
        "format": "json",
        "limit": limit
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return []

# Get place details
def get_place_details(xid):
    url = f"https://api.opentripmap.com/0.1/en/places/xid/{xid}"
    params = {"apikey": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return {}

# Store results
places_data = []

for dest in destinations:
    print(f"Fetching places for {dest['name']}...")
    places = get_places(dest["lat"], dest["lon"])
    for place in places:
        details = get_place_details(place["xid"])
        places_data.append({
            "destination_id": dest["destination_id"],
            "name": details.get("name", ""),
            "type": details.get("kinds", "").split(",")[0],  # use 1st kind
            "description": details.get("wikipedia_extracts", {}).get("text", ""),
            "rating": details.get("rate", 0),
            "duration_minutes": 60,  # default duration
            "latitude": details.get("point", {}).get("lat", 0),
            "longitude": details.get("point", {}).get("lon", 0)
        })
        time.sleep(1)  # avoid hitting rate limits

# Write to CSV
csv_file = "places.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "destination_id", "name", "type", "description",
        "rating", "duration_minutes", "latitude", "longitude"
    ])
    writer.writeheader()
    writer.writerows(places_data)

print(f"✅ Saved {len(places_data)} places to {csv_file}")

