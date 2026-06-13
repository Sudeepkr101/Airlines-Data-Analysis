import sqlite3
import json
from datetime import datetime, timedelta
import random

conn = sqlite3.connect('travel.sqlite')
cursor = conn.cursor()

# 1. aircrafts_data
cursor.execute('''CREATE TABLE IF NOT EXISTS aircrafts_data (
    aircraft_code TEXT,
    model TEXT,
    range INTEGER
)''')

aircrafts = [
    ('319', json.dumps({"en": "Airbus A319-100"}), 6700),
    ('320', json.dumps({"en": "Airbus A320-200"}), 5700),
    ('321', json.dumps({"en": "Airbus A321-200"}), 5600),
    ('733', json.dumps({"en": "Boeing 737-300"}), 4200),
    ('763', json.dumps({"en": "Boeing 767-300"}), 7900),
    ('773', json.dumps({"en": "Boeing 777-300"}), 11100),
    ('CN1', json.dumps({"en": "Cessna 208 Caravan"}), 1200),
    ('CR2', json.dumps({"en": "Bombardier CRJ-200"}), 2700),
    ('SU9', json.dumps({"en": "Sukhoi Superjet-100"}), 3000)
]
cursor.executemany('INSERT INTO aircrafts_data VALUES (?,?,?)', aircrafts)

# 2. airports_data
cursor.execute('''CREATE TABLE IF NOT EXISTS airports_data (
    airport_code TEXT,
    airport_name TEXT,
    city TEXT
)''')
airports = [
    ('JFK', json.dumps({"en": "John F. Kennedy International Airport"}), json.dumps({"en": "New York"})),
    ('LAX', json.dumps({"en": "Los Angeles International Airport"}), json.dumps({"en": "Los Angeles"}))
]
cursor.executemany('INSERT INTO airports_data VALUES (?,?,?)', airports)

# 3. seats
cursor.execute('''CREATE TABLE IF NOT EXISTS seats (
    aircraft_code TEXT,
    seat_no TEXT
)''')
seats_data = []
for ac in aircrafts:
    code = ac[0]
    num_seats = random.randint(121, 450)
    for i in range(num_seats):
        seats_data.append((code, f"{i}A"))
cursor.executemany('INSERT INTO seats VALUES (?,?)', seats_data)

# 4. bookings
cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
    book_ref TEXT,
    book_date TEXT,
    total_amount REAL
)''')
bookings_data = []
start_date = datetime(2023, 6, 22)
for i in range(100):
    date = start_date + timedelta(days=random.randint(0, 60))
    bookings_data.append((f"B{i}", date.strftime("%Y-%m-%d %H:%M:%S"), random.uniform(100, 1000)))
cursor.executemany('INSERT INTO bookings VALUES (?,?,?)', bookings_data)

# 5. tickets
cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
    ticket_no TEXT,
    book_ref TEXT
)''')
tickets_data = []
for i in range(100):
    tickets_data.append((f"T{i}", f"B{i}"))
cursor.executemany('INSERT INTO tickets VALUES (?,?)', tickets_data)

# 6. flights
cursor.execute('''CREATE TABLE IF NOT EXISTS flights (
    flight_id INTEGER,
    aircraft_code TEXT
)''')
flights_data = []
for i in range(10):
    flights_data.append((i, random.choice(aircrafts)[0]))
cursor.executemany('INSERT INTO flights VALUES (?,?)', flights_data)

# 7. boarding_passes
cursor.execute('''CREATE TABLE IF NOT EXISTS boarding_passes (
    ticket_no TEXT,
    flight_id INTEGER,
    boarding_no INTEGER
)''')
boarding_passes_data = []
for i in range(100):
    boarding_passes_data.append((f"T{i}", random.randint(0, 9), i))
cursor.executemany('INSERT INTO boarding_passes VALUES (?,?,?)', boarding_passes_data)

# 8. ticket_flights
cursor.execute('''CREATE TABLE IF NOT EXISTS ticket_flights (
    ticket_no TEXT,
    flight_id INTEGER,
    fare_conditions TEXT,
    amount REAL
)''')
ticket_flights_data = []
for i in range(100):
    ticket_flights_data.append((f"T{i}", random.randint(0, 9), random.choice(['Economy', 'Business', 'Comfort']), random.uniform(50, 500)))
cursor.executemany('INSERT INTO ticket_flights VALUES (?,?,?,?)', ticket_flights_data)

conn.commit()
conn.close()
