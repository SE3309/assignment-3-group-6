import pymysql
import random

# Database connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="BRATmusic"
)

cursor = db.cursor()

# Function to populate the userplaylistlibrary table
def populate_userplaylistlibrary(libraries=150):
    try:
        # Fetch all PlaylistIDs from the playlist table
        cursor.execute("SELECT PlaylistID FROM playlist")
        playlist_ids = [row[0] for row in cursor.fetchall()]

        if not playlist_ids:
            print("No playlists found in the playlist table. Please populate it first.")
            return

        print(f"Fetched {len(playlist_ids)} PlaylistIDs from the playlist table.")

        # Find the maximum LibraryID and start from the next available ID
        cursor.execute("SELECT COALESCE(MAX(LibraryID), 0) FROM userplaylistlibrary")
        start_library_id = cursor.fetchone()[0] + 1

        print(f"Starting LibraryID: {start_library_id}")

        # Generate libraries and assign 1-5 playlists to each
        for library_id in range(start_library_id, start_library_id + libraries):
            # Randomly decide the number of playlists for this library (1 to 5)
            num_playlists = random.randint(1, 5)
            # Randomly select PlaylistIDs for this library without duplication
            selected_playlists = random.sample(playlist_ids, min(num_playlists, len(playlist_ids)))

            for playlist_id in selected_playlists:
                # Check if this LibraryID and PlaylistID pair already exists
                cursor.execute(
                    "SELECT COUNT(*) FROM userplaylistlibrary WHERE LibraryID = %s AND PlaylistID = %s",
                    (library_id, playlist_id)
                )
                if cursor.fetchone()[0] > 0:
                    print(f"Skipping duplicate entry for LibraryID {library_id} and PlaylistID {playlist_id}")
                    continue

                # Insert into the table
                sql = "INSERT INTO userplaylistlibrary (LibraryID, PlaylistID) VALUES (%s, %s)"
                cursor.execute(sql, (library_id, playlist_id))

            print(f"LibraryID {library_id} populated with {len(selected_playlists)} playlists.")

        # Commit the changes
        db.commit()
        print(f"{libraries} libraries populated with 1-5 playlists each.")

    except pymysql.MySQLError as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

# Call the function
populate_userplaylistlibrary()
