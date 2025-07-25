import sqlite3, sqlalchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, create_engine, text, inspect
from IPython.display import Markdown, display
import csv

conn=sqlite3.connect("holiday_itinerary.db")
cursor=conn.cursor()

cursor.execute("""
    CREATE TABLE  IF NOT EXISTS destinations (
        destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        country TEXT,
        description TEXT,
        latitude REAL,
        longitude REAL
  );
""")

cursor.execute("""
    CREATE TABLE if not exists places (
        place_id INTEGER PRIMARY KEY AUTOINCREMENT,
        destination_id INTEGER,
        name text,
        type text, -- e.g., museum, park
        description TEXT,
        rating REAL,
        duration_minutes INTEGER,
        latitude REAL,
        longitude REAL,
        FOREIGN KEY (destination_id) REFERENCES destinations(destination_id)
     );
""")

cursor.execute("""
    CREATE TABLE if not exists events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        destination_id INTEGER,
        name text,
        category text, -- e.g., museum, park
        start_date DATE,
        end_date DATE,
        location text,
        description text,
        FOREIGN KEY (destination_id) REFERENCES destinations(destination_id)
     );
""")

cursor.execute("""
    CREATE TABLE if not exists accommodations (
        accommodation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        destination_id INTEGER,
        name text,
        address text, -- e.g., museum, park
        type text,
        price_per_night REAL,
        rating float,
        contact text,
        latitude REAL,
        longitude REAL,
        FOREIGN KEY (destination_id) REFERENCES destinations(destination_id)
     );
""")

cursor.execute("""
    CREATE TABLE if not exists transport (
        transport_id INTEGER PRIMARY KEY AUTOINCREMENT,
        destination_id INTEGER,
        type text,
        name text, 
        description text,
        start_location text,
        end_location text,
        price REAL,
        duration_minutes INTEGER,
        contact text,
        latitude REAL,
        longitude REAL,
        FOREIGN KEY (destination_id) REFERENCES destinations(destination_id)
     );
""")

'''
cursor.execute("""
     CREATE TABLE IF NOT EXISTS users (
       user_id INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT NOT NULL,
       email TEXT UNIQUE NOT NULL,
       password TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
""")
'''

conn.commit()
print("SQLITE table Destination created")

#Read csv and insert into table
with open("destinations.csv", "r", encoding="utf-8") as f:
    reader=csv.DictReader(f)
    row_inserted = 0
    for row in reader:
        cursor.execute("""
           insert into destinations(
           name, country, description, latitude, longitude)
           values (?, ?, ?, ?, ?)""", (
               row["name"],
               row["country"],
               row["description"],
               float(row["latitude"]) if row["latitude"] else None,
               float(row["longitude"]) if row["longitude"] else None
        ))
        row_inserted+=1

#Read csv and insert into table
with open("places.csv", "r", encoding="utf-8") as f:
    reader=csv.DictReader(f)
    row_inserted = 0
    for row in reader:
        cursor.execute("""
           insert into places(
           destination_id,name, type, description,rating,duration_minutes, latitude, longitude)
           values (?, ?, ?, ?, ?, ?, ?, ?)""", (
               int(row["destination_id"]),
               row["name"],
               row["type"],
               row["description"],
               row["rating"],
               row["duration_minutes"],
               float(row["latitude"]) if row["latitude"] else None,
               float(row["longitude"]) if row["longitude"] else None
        ))
        row_inserted+=1

#Read csv and insert into table
with open("events.csv", "r", encoding="utf-8") as f:
    reader=csv.DictReader(f)
    row_inserted = 0
    for row in reader:
        cursor.execute("""
           insert into events(
           destination_id, name, category, start_date, end_date, location, description
           ) VALUES (?, ?, ?, ?, ?, ?, ?)""", (
               int(row["destination_id"]),
               row["name"],
               row["category"],
               row["start_date"],
               row["end_date"],
               row["location"],
               row["description"]
                       ))
        row_inserted+=1

#Read csv and insert into table
#Read csv and insert into table
with open("accommodations.csv", "r", encoding="utf-8") as f:
    reader=csv.DictReader(f)
    row_inserted = 0
    for row in reader:
        cursor.execute("""
           insert into accommodations(
           destination_id,name, address, type, price_per_night, rating, contact, latitude, longitude)
           values (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
               int(row["destination_id"]),
               row["name"],
               row["name"],
               row["type"],
               row["price_per_night"],
               row["rating"],
               row["contact"],
               float(row["latitude"]) if row["latitude"] else None,
               float(row["longitude"]) if row["longitude"] else None
        ))
        row_inserted+=1

with open("transport.csv", "r", encoding="utf-8") as f:
    reader=csv.DictReader(f)
    row_inserted = 0
    for row in reader:
        cursor.execute("""
           insert into transport(
           destination_id, type, name, description, start_location, end_location, price, duration_minutes, contact,  latitude, longitude)
           values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
               int(row["destination_id"]),
               row["type"],
               row["name"],
               row["description"],
               row["start_location"],
               row["end_location"],
               row["price"],
               row["duration_minutes"],
               row["contact"],
               float(row["latitude"]) if row["latitude"] else None,
               float(row["longitude"]) if row["longitude"] else None
        ))
        row_inserted+=1

conn.commit()
conn.close()
print("All the tables has been created successfully")


