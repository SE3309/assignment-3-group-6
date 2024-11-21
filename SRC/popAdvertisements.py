import pymysql
import os
import random

# Database connection
connection = pymysql.connect(
    host="localhost",
    user="root",  # Replace with your DB username
    password="",  # Replace with your DB password
    database="BRATmusic"  # Replace with your database name
)

# Directory containing audio files
audio_dir = "audio"

try:
    with connection.cursor() as cursor:
        # Fetch all companies from the Advertiser table
        cursor.execute("SELECT company FROM Advertiser")
        advertisers = [row[0] for row in cursor.fetchall()]

        # Check if there are any companies in the Advertiser table
        if not advertisers:
            raise ValueError("No advertisers found in the Advertiser table. Please populate it first.")

        # Check if the audio directory exists
        if not os.path.exists(audio_dir):
            raise FileNotFoundError(f"The specified audio directory '{audio_dir}' does not exist.")

        # Loop through each audio file in the directory
        for file_name in os.listdir(audio_dir):
            file_path = os.path.join(audio_dir, file_name)

            # Check if the file is actually a file and not a directory
            if not os.path.isfile(file_path):
                print(f"Skipping '{file_name}' as it is not a file.")
                continue

            with open(file_path, "rb") as file:
                audio_data = file.read()

            # Randomly select a company from the fetched list
            company = random.choice(advertisers)

            # Generate a random cost for the advertisement
            cost = round(random.uniform(50.00, 500.00), 2)

            # Insert data into the Advertisement table
            sql = """
            INSERT INTO Advertisement (costOfAd, company, adFile)
            VALUES (%s, %s, %s)
            """
            try:
                cursor.execute(sql, (cost, company, audio_data))
            except pymysql.MySQLError as e:
                print(f"Error inserting advertisement for '{file_name}': {e}")
                continue

        # Commit the transaction
        connection.commit()
        print("Audio files inserted successfully into the Advertisement table!")

except FileNotFoundError as fe:
    print(f"Error: {fe}")
except ValueError as ve:
    print(f"Error: {ve}")
except pymysql.MySQLError as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # Ensure the database connection is closed
    if connection:
        connection.close()
