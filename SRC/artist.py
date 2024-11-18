import pymysql
import pandas as pd
import random
import string

# Database connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="sarah070920",
    database="BRATmusic"
)

cursor = db.cursor()

# Full path to the Excel file
excel_file = "./names.xlsx"

# Read Excel file
df = pd.read_excel(excel_file)

# Ensure the column 'names' exists
if 'names' not in df.columns:
    raise ValueError("The Excel file must have a column named 'names'.")

# Preprocess Excel data to remove duplicates
artist_names = df['names'].dropna().drop_duplicates().tolist()

# Function to generate random email


def random_email():
    domains = ["example.com", "music.com", "artistmail.com", "mail.com"]
    return f"{''.join(random.choices(string.ascii_letters + string.digits, k=8))}@{random.choice(domains)}"

# Function to insert data into the database


def populate_artist_table(names):
    for name in names:
        # Check if the name already exists in the database
        cursor.execute(
            "SELECT COUNT(*) FROM Artist WHERE artistName = %s", (name,))
        if cursor.fetchone()[0] > 0:  # Name exists, skip it
            print(f"Skipping duplicate: {name}")
            continue

        # Generate other data fields
        total_duration = random.randint(
            10000, 1000000)  # Random total duration
        revenue_generated = round(random.uniform(
            50000, 2000000), 2)  # Random revenue
        email = random_email()
        password = ''.join(random.choices(
            string.ascii_letters + string.digits, k=12))  # Random password

        # SQL query
        sql = "INSERT INTO Artist (artistName, totalDurationListenedTo, revenueGenerated, email, password) VALUES (%s, %s, %s, %s, %s)"
        values = (name, total_duration, revenue_generated, email, password)

        # Execute query
        cursor.execute(sql, values)

    # Commit the changes
    db.commit()
    print(f"{len(names)} rows processed (duplicates skipped).")


# Call the function
populate_artist_table(artist_names)

# Close the connection
cursor.close()
db.close()
