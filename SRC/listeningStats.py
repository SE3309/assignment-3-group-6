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

# Function to populate ListeningStats table
def populate_listening_stats(rows=200):
    try:
        # Fetch all userIDs from the User table
        cursor.execute("SELECT email FROM User")
        user_ids = [row[0] for row in cursor.fetchall()]

        # Fetch all mediaIDs from the Media table
        cursor.execute("SELECT MediaID FROM Media")
        media_ids = [row[0] for row in cursor.fetchall()]

        if not user_ids or not media_ids:
            print("User or Media table is empty! Please populate them first.")
            return

        print(f"Fetched {len(user_ids)} userIDs and {len(media_ids)} mediaIDs.")

        used_combinations = set()  # To ensure unique userID-mediaID pairs

        for _ in range(rows):
            # Generate a unique userID-mediaID combination
            while True:
                user_id = random.choice(user_ids)
                media_id = random.choice(media_ids)
                if (user_id, media_id) not in used_combinations:
                    used_combinations.add((user_id, media_id))
                    break

            # Generate a random duration (1 to 3600 seconds)
            duration = random.randint(1, 60)

            # Insert the row into the ListeningStats table
            sql = """
            INSERT INTO ListeningStats (userID, mediaID, duration)
            VALUES (%s, %s, %s)
            """
            values = (user_id, media_id, duration)

            try:
                cursor.execute(sql, values)
            except pymysql.MySQLError as e:
                print(f"Error inserting {values}: {e}")
                continue

        # Commit changes to the database
        db.commit()
        print(f"{rows} rows inserted into the ListeningStats table.")

    except pymysql.MySQLError as err:
        print(f"Database error: {err}")
    finally:
        # Close the cursor and database connection
        cursor.close()
        db.close()

# Call the function to populate the table
populate_listening_stats()
