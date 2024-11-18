import pymysql
import os
import random

# Database connection
connection = pymysql.connect(
    host="localhost",
    user="root",  # Replace with your DB username
    password="sarah070920",  # Replace with your DB password
    database="BRATmusic"  # Replace with your database name
)

# Directory containing audio files
audio_dir = "audio"

try:
    with connection.cursor() as cursor:
        # Fetch all companies from the Advertiser table
        cursor.execute("SELECT company FROM Advertiser")
        advertisers = [row[0] for row in cursor.fetchall()]

        # Loop through each audio file
        for file_name in os.listdir(audio_dir):
            file_path = os.path.join(audio_dir, file_name)
            with open(file_path, "rb") as file:
                audio_data = file.read()

            # Randomly select a company from the fetched list
            company = random.choice(advertisers)

            # Generate a random cost
            cost = round(random.uniform(50.00, 500.00), 2)

            # Insert data into Advertisement table
            sql = """
            INSERT INTO Advertisement (costOfAd, company, adFile)
            VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (cost, company, audio_data))

        # Commit the transaction
        connection.commit()
        print("Audio files inserted successfully into the Advertisement table!")

finally:
    connection.close()
