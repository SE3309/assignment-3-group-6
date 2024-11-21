import pymysql
import os
import random
from datetime import datetime, timedelta

# Database connection details
connection = pymysql.connect(
    host="localhost",
    user="root",  # Your MySQL username
    password="",  # Your MySQL password
    database="BRATmusic"  # Your database name
)

print("Connected to the database!")

# Directory containing MP3 files
media_dir = "music"

rowNum = 2000  # Total number of rows to insert

try:
    # Creating cursor
    cursor = connection.cursor()

    # Fetching albumIDs from the Album table
    cursor.execute("SELECT albumID FROM Album")
    album_ids = [row[0] for row in cursor.fetchall()]  # Extract albumIDs as a list

    # Fetching artistNames from the Artist table
    cursor.execute("SELECT artistName FROM Artist")
    artist_names = [row[0] for row in cursor.fetchall()]  # Extract artistNames as a list

    if not album_ids or not artist_names:
        raise ValueError("No albumIDs or artistNames found in the database.")

    print(f"Found {len(album_ids)} album IDs and {len(artist_names)} artist names.")
    print(f"Populating the Media table with {rowNum} rows...")

    # Fetching MP3 files
    if not os.path.exists(media_dir):
        raise FileNotFoundError(f"The specified folder '{media_dir}' does not exist.")
    
    mp3_files = [f for f in os.listdir(media_dir) if os.path.isfile(os.path.join(media_dir, f))]
    if not mp3_files:
        raise FileNotFoundError("No MP3 files found in the specified folder.")

    print(f"Found {len(mp3_files)} MP3 files in the folder.")

    # Loop to insert rows into the Media table
    for i in range(rowNum):
        # Select random albumID, artistName, and MP3 file
        album_id = random.choice(album_ids)
        artist_name = random.choice(artist_names)
        selected_file = random.choice(mp3_files)
        file_path = os.path.join(media_dir, selected_file)

        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > 50 * 1024 * 1024:  # Skip files larger than 50 MB
            print(f"Skipping '{selected_file}' (File too large: {file_size} bytes)")
            continue

        print(f"File size of '{selected_file}': {file_size} bytes")

        # Read binary data from the file
        with open(file_path, "rb") as file:
            audio_data = file.read()

        # Generate random values for additional columns
        length_of_media = random.randint(60, 600)  # 1 to 10 minutes
        media_ranking = random.randint(1, 10)      # Ranking between 1 and 10
        date_created = datetime.now() - timedelta(days=random.randint(0, 1825))  # Random date in the last 5 years
        total_duration_listened_to = random.randint(100, 50000)  # Between 100 and 50,000 seconds

        # Insert the row into the Media table
        sql = """
        INSERT INTO Media (mediaName, mediaFile, totalDurationListenedTo, mediaRanking, dateCreated, lengthOfMedia, albumID, artistName)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(sql, (
                selected_file,
                audio_data,
                total_duration_listened_to,
                media_ranking,
                date_created.strftime('%Y-%m-%d %H:%M:%S'),
                length_of_media,
                album_id,
                artist_name
            ))
        except pymysql.IntegrityError as e:
            print(f"IntegrityError: {e} for albumID: {album_id}, artistName: {artist_name}")
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

        # Commit every 100 rows to avoid locking issues
        if (i + 1) % 100 == 0:
            connection.commit()
            print(f"Inserted {i + 1} rows so far...")

    # Final commit after the loop
    connection.commit()
    print(f"Table successfully populated with {rowNum} rows!")

except FileNotFoundError as fe:
    print(f"Error: {fe}")
except ValueError as ve:
    print(f"Error: {ve}")
except pymysql.MySQLError as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # Closing the database connection
    if connection:
        connection.close()
