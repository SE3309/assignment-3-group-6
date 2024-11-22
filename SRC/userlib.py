import mysql.connector
import random

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="BRATmusic"
)

cursor = db.cursor()

# Function to populate the userplaylistlibrary table
def populate_userplaylistlibrary(entries=150):
    try:
        # Fetch all PlaylistIDs from the playlist table
        cursor.execute("SELECT PlaylistID FROM playlist")
        playlist_ids = [row[0] for row in cursor.fetchall()]

        if not playlist_ids:
            print("No playlists found in the playlist table. Please populate it first.")
            return

        print(f"Fetched {len(playlist_ids)} PlaylistIDs from the playlist table.")

        # Generate libraries and assign playlists
        for library_id in range(1, entries + 1):  # Library IDs start from 1
            # Randomly decide the number of playlists for this library (1 to 5)
            num_playlists = random.randint(1, 5)
            # Randomly select PlaylistIDs for this library without duplication
            selected_playlists = random.sample(playlist_ids, min(num_playlists, len(playlist_ids)))

            for playlist_id in selected_playlists:
                # Insert into the table
                sql = "INSERT INTO userplaylistlibrary (LibraryID, PlaylistID) VALUES (%s, %s)"
                try:
                    cursor.execute(sql, (library_id, playlist_id))
                except mysql.connector.Error as e:
                    print(f"Error inserting (LibraryID: {library_id}, PlaylistID: {playlist_id}): {e}")
                    continue

            print(f"LibraryID {library_id} populated with {len(selected_playlists)} playlists.")

        # Commit the changes
        db.commit()
        print(f"{entries} libraries populated successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

# Call the function
populate_userplaylistlibrary()
