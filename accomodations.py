import requests
import csv
import time

API_KEY = "5ae2e3f221c38a28845f05b61e162e10abf26414177bb9336af43455"

destinations = [
    {"destination_id": 1, "name": "Paris", "latitude": 48.8566, "longitude": 2.3522},
    {"destination_id": 2, "name": "Rome", "latitude": 41.9028, "longitude": 12.4964},
    {"destination_id": 3, "name": "Zurich", "latitude": 47.3769, "longitude": 8.5417},
]

def fetch_accommodations(lat, lon, radius=10000):
    url = "https://api.opentripmap.com/0.1/en/places/radius"
    params = {
        "apikey": API_KEY,
        "radius": radius,
        "lat": lat,
        "lon": lon,
        "kinds": "accomodations",
        "limit": 50,
        "format": "json"
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        return r.json()
    else:
        print(f"Error {r.status_code} fetching accommodations")
        return []

accommodations = []
for dest in destinations:
    print(f"Fetching accommodations for {dest['name']}...")
    places = fetch_accommodations(dest["latitude"], dest["longitude"])
    for place in places:
        address = place.get("address", {})
        accommodations.append({
            "destination_id": dest["destination_id"],
            "name": place.get("name", ""),
            "address": f"{address.get('road', '')}, {address.get('city', '')}".strip(", "),
            "type": place.get("kinds", "").split(",")[0],
            "price_per_night": "",  # not provided by API
            "rating": "",           # not provided by API
            "contact": "",          # not provided by API
            "latitude": place.get("point", {}).get("lat", 0),
            "longitude": place.get("point", {}).get("lon", 0)
        })
    time.sleep(1)  # be kind to API

with open("accommodations.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["destination_id","name","address","type","price_per_night","rating","contact","latitude","longitude"])
    writer.writeheader()
    writer.writerows(accommodations)

print(f"Saved {len(accommodations)} accommodations to accommodations.csv")
