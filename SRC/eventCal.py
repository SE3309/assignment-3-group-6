import random
from datetime import datetime, timedelta
import pymysql

# Database connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="BRATmusic"
)

cursor = db.cursor()

# Function to generate a random time
def random_time():
    return f"{random.randint(0, 23):02}:{random.randint(0, 59):02}:{random.randint(0, 59):02}"

# Function to generate a random location
def random_location():
    cities = ["New York", "Los Angeles", "London", "Paris", "Berlin", "Tokyo", "Sydney", "Mumbai", "Dubai", "Rio de Janeiro"]
    return random.choice(cities)

# Function to populate the eventcalendar table with data from the album table
def populate_eventcalendar_table(events=100):
    # Fetch data from the album table
    cursor.execute("SELECT artistName, albumID, dateCreated FROM album")
    album_data = cursor.fetchall()

    if not album_data:
        print("No data found in the album table. Please check the table and try again.")
        return

    # Generate 100 events
    for _ in range(events):
        # Randomly select an album
        artistName, albumID, dateCreated = random.choice(album_data)

        # Generate random event details
        eventDate = dateCreated + timedelta(days=random.randint(1, 365))  # Event date is after album creation
        eventTime = random_time()
        location = random_location()
        revenueGenerated = round(random.uniform(1000, 100000), 2)  # Random revenue

        # SQL query to insert into eventcalendar table
        sql = """
            INSERT INTO eventcalendar (artistName, eventDate, eventTime, location, revenueGenerated)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (artistName, eventDate, eventTime, location, revenueGenerated)

        # Execute query
        cursor.execute(sql, values)

    # Commit the changes
    db.commit()
    print(f"{events} rows inserted into the eventcalendar table.")

# Call the function
populate_eventcalendar_table()

# Close the connection
cursor.close()
db.close()
