import pymysql
import pandas as pd
import random
from datetime import datetime, timedelta

# Load songs and artists from Excel
excel_file = 'real_songs_artists.xlsx'
df = pd.read_excel(excel_file)  # Assumes Excel file has 'SongName' and 'ArtistName' columns
song_artist_data = df.to_dict('records')  # Convert to list of dictionaries

# Define the number of rows to update
rowNum = 1008  # Adjust this value based on your dataset

# Database connection
connection = pymysql.connect(
    host="localhost",
    user="root",  # Replace with your DB username
    password="Shadowflash1",  # Replace with your DB password
    database="BRATmusic"  # Replace with your database name
)

# Validate the number of rows in the Excel file
if len(song_artist_data) < rowNum:
    raise ValueError(f"Excel file contains only {len(song_artist_data)} songs, but {rowNum} rows are required.")

# Create cursor
cursor = connection.cursor()

# Iterate through song_artist_data to update the database
for i in range(rowNum):
    song_entry = song_artist_data[i % len(song_artist_data)]  # Loop through the Excel data
    media_name = song_entry['SongName']
    artist_name = song_entry['ArtistName']
    media_id = i + 1  # Assuming mediaID starts at 1 and is sequential

    # Update the row in the Media table
    sql = """
    UPDATE Media
    SET mediaName = %s, artistName = %s
    WHERE mediaID = %s
    """
    try:
        cursor.execute(sql, (
            media_name,
            artist_name,
            media_id
        ))
    except Exception as e:
        print(f"Error updating mediaID {media_id}: {e}")
        continue

    # Commit every 100 rows for efficiency
    if (i + 1) % 100 == 0:
        connection.commit()
        print(f"Updated {i + 1} rows so far...")

# Final commit and cleanup
connection.commit()
connection.close()
print("Database update complete!")
