import requests
import csv

# Step 1: API endpoint for DummyJSON user data
url = "https://dummyjson.com/users"

# Step 2: Request data
response = requests.get(url)
data = response.json()

# Step 3: Extract and format user data
users = []

for user in data["users"]:  # Corrected from 'results' to 'users'
    users.append({
        "user_id": user["id"],
        "name": f"{user['firstName']} {user['lastName']}",
        "email": user["email"],
        "country": user["address"]["country"],
        "username": user["username"],
        "age": user["age"]
    })

# Step 4: Save to CSV
csv_file = "users.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["user_id", "name", "email", "country", "username", "age"])
    writer.writeheader()
    writer.writerows(users)

print(f"✅ Saved {len(users)} users to {csv_file}")
