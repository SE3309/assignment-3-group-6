import pandas as pd
from faker import Faker
import mysql.connector
import random

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="BRATmusic"
)

# Load the Excel file
file_path = r'\names.xlsx'
user_data = pd.read_excel(file_path, engine='openpyxl')

# Initialize Faker for generating random data
fake = Faker()

# List of email domains
email_domains = ["example.com", "music.com", "bratmusic.com", "mail.com"]

# Database cursor
cursor = db.cursor()

# Fetch all available LibraryIDs from the userplaylistlibrary table
cursor.execute("SELECT LibraryID FROM userplaylistlibrary")
available_library_ids = [row[0] for row in cursor.fetchall()]

# SQL insert query for the user table
insert_user_query = """
INSERT INTO user (UserID, DisplayName, StartDateOfSubscription, Password, SubscriptionType, PlaylistLibraryID)
VALUES (%s, %s, %s, %s, %s, %s)
"""

# Check if UserID already exists
check_user_id_query = "SELECT COUNT(*) FROM user WHERE UserID = %s"

for index, row in user_data.iterrows():
    # Ensure the 'names' column exists and is not empty
    if pd.isnull(row['names']):
        continue  # Skip rows with missing values in 'names'

    # Create an email address using the name and a random domain
    name_part = row['names'].lower().replace(" ", ".")  # Replace spaces with dots for email format
    email = f"{name_part}@{random.choice(email_domains)}"
    user_id = email  # Use email as UserID

    # Check if the UserID (email) already exists
    cursor.execute(check_user_id_query, (user_id,))
    user_id_exists = cursor.fetchone()[0]

    if user_id_exists:  # Skip this record if the UserID already exists
        print(f"Skipping duplicate UserID (email): {user_id}")
        continue

    display_name = row['names']  # Use 'names' column as DisplayName
    start_date_of_subscription = fake.date_between(start_date='-2y', end_date='today')  # Random subscription date
    password = fake.password(length=10)  # Randomly generated password
    subscription_type = fake.random_element(elements=('Premium', 'Free'))  # Valid values for SubscriptionType

    # Assign a unique PlaylistLibraryID to the user, or set it to NULL if no libraries are left
    if available_library_ids:
        playlist_library_id = available_library_ids.pop(0)  # Assign the first available LibraryID
    else:
        playlist_library_id = None  # No more libraries left, set to NULL

    # Insert the user into the user table
    cursor.execute(insert_user_query, (
        user_id, display_name, start_date_of_subscription, password, subscription_type, playlist_library_id
    ))

    # Print user details for debugging
    print(f"Inserted User: {display_name}, Email: {email}, UserID: {user_id}, LibraryID: {playlist_library_id}")

# Commit changes to the database
db.commit()

# Close the cursor and the database connection
cursor.close()
db.close()

print("Data from names.xlsx has been successfully inserted into the user table with unique PlaylistLibraryIDs or NULL where no libraries were available.")
