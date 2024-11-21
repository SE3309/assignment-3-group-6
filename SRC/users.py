import pandas as pd
from faker import Faker
import pymysql

# Load the Excel file
file_path = 'userINFO.xlsx'  # Assuming the file is in the same directory as the script
user_data = pd.read_excel(file_path)

# Initialize Faker for generating random data
fake = Faker()

# Add a new column for user emails
user_data['email'] = [fake.unique.email() for _ in range(len(user_data))]

# Save the updated DataFrame back to the Excel file
user_data.to_excel(file_path, index=False)
print(f"Updated userINFO.xlsx with emails.")

# Database connection using pymysql
db = pymysql.connect(
    host="localhost",
    user="root",  # Replace with your username
    password="",  # Replace with your password
    database="BRATmusic"  # Replace with your database name
)
cursor = db.cursor()

# Fetch the current maximum LibraryID from the userplaylistlibrary table
cursor.execute("SELECT MAX(LibraryID) FROM userplaylistlibrary")
result = cursor.fetchone()
max_library_id = result[0] if result[0] is not None else 0  # Start at 0 if table is empty

# SQL insert query for the User table
insert_query = """
INSERT INTO User (email, display_name, start_date_of_subscription, password, subscription_type_id, playlist_library_id)
VALUES (%s, %s, %s, %s, %s, %s)
"""

# Check if email already exists
check_email_query = "SELECT COUNT(*) FROM User WHERE email = %s"

# Start generating unique playlist_library_ids
unique_library_id = max_library_id + 1

for index, row in user_data.iterrows():
    if pd.isnull(row['UserName']) or pd.isnull(row['names']):
        continue  # Skip rows with missing values

    email = fake.unique.email()  # Use the email from the new column
    cursor.execute(check_email_query, (email,))
    email_exists = cursor.fetchone()[0]

    if email_exists:  # Skip this record if the email already exists
        print(f"Skipping duplicate email: {email}")
        continue

    display_name = row['names']  # Use 'names' column as display_name
    start_date_of_subscription = fake.date_between(start_date='-2y', end_date='today')  # Random subscription date
    password = fake.password(length=10)  # Randomly generated password
    subscription_type_id = fake.random_element(elements=('Premium', 'Free'))  # Valid values from SubscriptionTiers

    # Assign a unique playlist_library_id
    playlist_library_id = unique_library_id
    unique_library_id += 1  # Increment for the next user

    # Execute the SQL insert statement
    cursor.execute(insert_query, (
        email, display_name, start_date_of_subscription, password, subscription_type_id, playlist_library_id
    ))

# Commit changes to the database
db.commit()

# Close the cursor and the database connection
cursor.close()
db.close()

print("Data from userINFO.xlsx has been successfully inserted into the User table with unique playlist_library_ids.")
