import requests
import csv

# Step 1: API endpoint for mock user data
url = "https://randomuser.me/api/?results=10&nat=us,gb,fr,it,ch"

# Step 2: Request data
response = requests.get(url)
data = response.json()

# Step 3: Extract and format user data
users = []

for user in data["results"]:
    users.append({
        "user_id": None,  # Use None for SQLite auto-increment
        "name": f"{user['name']['first']} {user['name']['last']}",
        "email": user["email"],
        "country": user["location"]["country"],
        "preferred_destination": "",  # Can fill manually or generate
        "registered_date": user["registered"]["date"].split("T")[0]
    })

# Step 4: Save to CSV
csv_file = "users.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["user_id", "name", "email", "country", "preferred_destination", "registered_date"])
    writer.writeheader()
    writer.writerows(users)

print(f"✅ Saved {len(users)} users to {csv_file}")

