import pymysql
import os
import random

# Connecting to the database
connection = pymysql.connect(
    host="localhost",        # Database host
    user="root",             # MySQL username
    password="sarah070920",  # MySQL password
    database="BRATmusic"   # Database name
)

print("Connected to the database!")

# Directory containing MP3 files
media_dir = "./music"  # Replace with the actual path if needed

rowNum = 2000  # Total number of rows to insert

try:
    # Creating cursor
    cursor = connection.cursor()

    # Fetching files
    mp3_files = os.listdir(media_dir)
    if not mp3_files:
        raise FileNotFoundError("No MP3 files found in the specified folder.")

    print(
        f"Found {len(mp3_files)} MP3 files in the folder. Populating the table with {rowNum} rows...")

    # Looping to insert rows one at a time
    for i in range(rowNum):
        # Select random MP3 file and read binary data
        selected_file = random.choice(mp3_files)
        file_path = os.path.join(media_dir, selected_file)

        # Check file size (ensure it's not too large)
        file_size = os.path.getsize(file_path)
        print(f"File size of {selected_file}: {file_size} bytes")

        with open(file_path, "rb") as file:
            audio_data = file.read()

        # Insert the row into the database
        sql = """
        INSERT INTO Media (mediaName, mediaFile)
        VALUES (%s, %s)
        """
        cursor.execute(sql, (selected_file, audio_data))
        connection.commit()

        if (i + 1) % 100 == 0 or i + 1 == rowNum:
            print(f"Inserted {i + 1} rows so far...")

    print("Table successfully populated with 2000 rows!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Closing the database connection
    if connection:
        connection.close()
