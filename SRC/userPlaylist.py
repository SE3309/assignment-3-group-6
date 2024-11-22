import random
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta

# Load playlist descriptions from the Excel file
file_path = r'C:\Users\kauro\Desktop\3309\BRATmusic\assignment-3-group-6\SRC\ps.xlsx'
data = pd.read_excel(file_path)
playlist_descriptions = data['playlist'].dropna().tolist()  # Drop any missing values

# Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Replace with your database password
    database="BRATmusic"  # Replace with your database name
)

cursor = db.cursor()

# Function to generate random dates
def random_date(start_year=2000, end_year=2023):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

# Function to populate the playlist table
def populate_playlist_table(rows=200):
    # Fetch all MediaID from the media table
    cursor.execute("SELECT MediaID FROM media")
    media_ids = [row[0] for row in cursor.fetchall()]
    
    # Fetch all UserId from the User table
    cursor.execute("SELECT UserId FROM user")
    user_ids = [row[0] for row in cursor.fetchall()]
    
    # Fetch the current maximum PlaylistID from the playlist table
    cursor.execute("SELECT MAX(PlaylistID) FROM playlist")
    max_playlist_id = cursor.fetchone()[0] or 0  # Start from 0 if the table is empty

    if not media_ids or not user_ids:
        print("Media or User table is empty!")
        return

    for i in range(1, rows + 1):
        playlist_id = max_playlist_id + i  # Generate a unique PlaylistID
        description = random.choice(playlist_descriptions)  # Random playlist description
        media_id = random.choice(media_ids)  # Random MediaID
        user_id = random.choice(user_ids)  # Random UserId (Creator)
        date_added = random_date().strftime('%Y-%m-%d')  # Random date

        # SQL query to insert data into the playlist table
        sql = """
        INSERT INTO playlist (PlaylistID, Description, MediaID, Creator, DateAdded)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (playlist_id, description, media_id, user_id, date_added)

        # Execute the query
        try:
            cursor.execute(sql, values)
        except mysql.connector.Error as e:
            print(f"Error inserting {values}: {e}")
            continue

    # Commit the changes
    db.commit()
    print(f"{rows} rows inserted into the playlist table.")

# Call the function to populate the playlist table
populate_playlist_table()

# Close the connection
cursor.close()
db.close()
