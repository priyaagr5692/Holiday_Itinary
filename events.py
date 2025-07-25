import requests
import csv
import time
import os

API_KEY = "w75TvodGt35ZLQSWYQeP6XrmwE9Y0Wac"  # <-- Replace with your actual API Key

destinations = [
    {"destination_id": 1, "city": "Paris"},
    {"destination_id": 2, "city": "Rome"},
    {"destination_id": 3, "city": "Zurich"}
]

events_data = []

def get_events(city_name):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": API_KEY,
        "city": city_name,
        "size": 20,
        "sort": "date,asc"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("_embedded", {}).get("events", [])
    else:
        print(f"❌ Error fetching events for {city_name}: {response.status_code}")
        return []

for dest in destinations:
    print(f"📍 Fetching events for {dest['city']}...")
    events = get_events(dest["city"])

    for e in events:
        start_date = e.get("dates", {}).get("start", {}).get("localDate", "")
        end_date = start_date  # Ticketmaster doesn’t provide end date in all cases
        venue = e.get("_embedded", {}).get("venues", [{}])[0].get("name", "")
        description = e.get("info", "") or e.get("pleaseNote", "")

        events_data.append({
            "destination_id": dest["destination_id"],
            "name": e.get("name", ""),
            "category": e.get("classifications", [{}])[0].get("segment", {}).get("name", "General"),
            "start_date": start_date,
            "end_date": end_date,
            "location": venue,
            "description": description
        })

    time.sleep(1)  # rate limit friendly

# Save to CSV
if os.path.exists("events.csv"):
  os.remove("events.csv")
else:
  print("The file does not exist")

csv_file = "events.csv"

with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "destination_id", "name", "category", "start_date",
        "end_date", "location", "description"
    ])
    writer.writeheader()
    writer.writerows(events_data)

print(f"✅ {len(events_data)} events saved to {csv_file}")

