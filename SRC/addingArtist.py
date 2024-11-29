import pymysql
import pandas as pd
import random
import string

# Load songs and artists from Excel
excel_file = 'real_songs_artists.xlsx'
df = pd.read_excel(excel_file)  # Assumes Excel file has 'SongName' and 'ArtistName' columns
song_artist_data = df.to_dict('records')  # Convert to list of dictionaries

# Database connection
connection = pymysql.connect(
    host="localhost",
    user="root",  # Replace with your DB username
    password="Shadowflash1",  # Replace with your DB password
    database="BRATmusic"  # Replace with your database name
)

# Create cursor
cursor = connection.cursor()

# Function to generate random email
def generate_random_email():
    domains = ['@mail.com', '@music.com', '@artistmail.com', '@example.com']
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + random.choice(domains)

# Function to generate random password
def generate_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

# Step 1: Temporarily disable foreign key checks
print("Disabling foreign key checks...")
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

# Step 2: Clear the `Artist` table
print("Clearing the Artist table...")
cursor.execute("TRUNCATE TABLE Artist")
print("Artist table cleared successfully!")

# Step 3: Re-enable foreign key checks
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# Step 4: Insert updated data into the `Artist` table
print("Inserting updated data into the Artist table...")
for entry in song_artist_data:
    artist_name = entry['ArtistName']
    total_duration_listened_to = random.randint(10000, 1000000)  # Random duration between 10,000 and 1,000,000
    revenue_generated = round(random.uniform(1000.0, 1000000.0), 2)  # Random revenue between 1,000 and 1,000,000
    email = generate_random_email()
    password = generate_random_password()

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

# Step 5: Commit changes to the database
connection.commit()
connection.close()

print("All artist data replaced successfully!")
