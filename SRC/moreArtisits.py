import pymysql
import pandas as pd
import random
import string

# Load new artist data from the Excel file
excel_file = 'real_artists_500.xlsx'  # Replace with the correct path to the new Excel file
df = pd.read_excel(excel_file)  # Assumes columns: ArtistName, TotalDurationListenedTo, RevenueGenerated, Email, Password
new_artist_data = df.to_dict('records')  # Convert to a list of dictionaries

# Database connection
connection = pymysql.connect(
    host="localhost",
    user="root",  # Replace with your DB username
    password="Shadowflash1",  # Replace with your DB password
    database="BRATmusic"  # Replace with your database name
)

# Create cursor
cursor = connection.cursor()

# Insert new artists into the Artist table if they don't already exist
print("Adding new artists to the Artist table...")
for entry in new_artist_data:
    artist_name = entry['ArtistName']
    total_duration_listened_to = entry['TotalDurationListenedTo']
    revenue_generated = entry['RevenueGenerated']
    email = entry['Email']
    password = entry['Password']

    # Check if the artist already exists
    cursor.execute("SELECT * FROM Artist WHERE artistName = %s", (artist_name,))
    result = cursor.fetchone()

    if not result:
        try:
            # Insert new artist data
            sql_insert_artist = """
            INSERT INTO Artist (artistName, totalDurationListenedTo, revenueGenerated, email, password)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insert_artist, (
                artist_name,
                total_duration_listened_to,
                revenue_generated,
                email,
                password
            ))
            print(f"Inserted new artist: {artist_name}")
        except Exception as e:
            print(f"Error inserting artist '{artist_name}': {e}")
    else:
        print(f"Artist '{artist_name}' already exists, skipping...")

# Commit changes to the database
connection.commit()
connection.close()

print("New artists added successfully!")
