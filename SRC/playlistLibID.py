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
def populate_userplaylistlibrary():
    try:
        # Fetch all PlaylistIDs from the playlist table
        cursor.execute("SELECT PlaylistID FROM playlist")
        playlist_ids = [row[0] for row in cursor.fetchall()]

        if not playlist_ids:
            print("No playlists found in the playlist table. Please populate it first.")
            return

        print(f"Fetched {len(playlist_ids)} PlaylistIDs from the playlist table.")

        # Start generating unique LibraryIDs
        cursor.execute("SELECT COALESCE(MAX(LibraryID), 0) FROM userplaylistlibrary")
        next_library_id = cursor.fetchone()[0] + 1

        # Track used playlists to ensure uniqueness per library
        used_playlists = set()

        # Generate libraries and assign unique playlists to each
        libraries_to_create = 150  # Number of new libraries to create
        for _ in range(libraries_to_create):
            # Randomly decide the number of playlists for this library (1 to 5)
            num_playlists = random.randint(1, 5)
            
            # Select unique PlaylistIDs for this library
            available_playlists = list(set(playlist_ids) - used_playlists)
            if len(available_playlists) < num_playlists:
                print("Not enough unique playlists available for new libraries.")
                break
            
            selected_playlists = random.sample(available_playlists, num_playlists)

            for playlist_id in selected_playlists:
                # Insert each PlaylistID with the new LibraryID
                sql = "INSERT INTO userplaylistlibrary (LibraryID, PlaylistID) VALUES (%s, %s)"
                cursor.execute(sql, (next_library_id, playlist_id))

                # Add the playlist to the used set
                used_playlists.add(playlist_id)

            print(f"LibraryID {next_library_id} populated with {len(selected_playlists)} unique playlists.")
            next_library_id += 1  # Increment LibraryID for the next library

        # Commit the changes
        db.commit()
        print(f"{libraries_to_create} libraries populated with unique playlists.")

    except pymysql.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

# Call the function
populate_userplaylistlibrary()
