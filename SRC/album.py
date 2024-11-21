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

# Function to generate random dates
def random_date(start_year=2000, end_year=2023):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

# Function to populate the Album table
def populate_album_table(rows=150):  # Set rows to 150
    # Fetch all artist names from the Artist table
    cursor.execute("SELECT artistName FROM Artist")
    artist_names = [row[0].strip().lower() for row in cursor.fetchall()]  # Normalize case and trim spaces

    if not artist_names:
        print("No artists found in the Artist table!")
        return

    for _ in range(rows):
        artist_name = random.choice(artist_names)  # Ensure the artist name exists in Artist table
        date_created = random_date()

        # SQL query to insert data into the Album table
        sql = "INSERT INTO Album (artistName, dateCreated) VALUES (%s, %s)"
        values = (artist_name, date_created.strftime('%Y-%m-%d'))
        
        # Debugging: Print values before inserting
        print(f"Inserting: {values}")
        
        # Execute the query
        try:
            cursor.execute(sql, values)
        except mysql.connector.Error as e:
            print(f"Error inserting {values}: {e}")
            continue

    # Commit the changes
    db.commit()
    print(f"{rows} rows inserted into the Album table.")

# Call the function to populate the Album table
populate_album_table()  # Generates 150 rows

# Close the connection
cursor.close()
db.close()
