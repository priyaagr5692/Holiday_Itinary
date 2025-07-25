import requests
import csv

API_KEY = "5ae2e3f221c38a28845f05b61e162e10abf26414177bb9336af43455"

# List of cities (you can modify or load from a file)
destinations = [
    {"name": "Paris", "country": "France"},
    {"name": "Rome", "country": "Italy"},
    {"name": "Zurich", "country": "Switzerland"},
    {"name": "Amsterdam", "country": "Netherlands"},
    {"name": "Barcelona", "country": "Spain"}
]

# Geocoding + Wikipedia description
def get_location_data(city_name, country):
    geo_url = "https://api.opentripmap.com/0.1/en/places/geoname"
    params = {
        "apikey": API_KEY,
        "name": city_name
    }
    geo_resp = requests.get(geo_url, params=params)
    if geo_resp.status_code != 200:
        return None
    geo_data = geo_resp.json()

    lat = geo_data.get("lat", 0)
    lon = geo_data.get("lon", 0)
    desc = geo_data.get("wikidata", "")

    return {
        "name": city_name,
        "country": country,
        "description": geo_data.get("wikipedia_extracts", {}).get("text", ""),
        "latitude": lat,
        "longitude": lon
    }

# Fetch data for each destination
destination_records = []
for dest in destinations:
    data = get_location_data(dest["name"], dest["country"])
    if data:
        destination_records.append(data)

# Save to CSV
csv_file = "destinations.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "country", "description", "latitude", "longitude"])
    writer.writeheader()
    writer.writerows(destination_records)

print(f"✅ Saved {len(destination_records)} destinations to {csv_file}")

