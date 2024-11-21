import pymysql
import pandas as pd
import random
import string

# Function to generate random email
def random_email():
    domains = ["example.com", "music.com", "artistmail.com", "mail.com"]
    return f"{''.join(random.choices(string.ascii_letters + string.digits, k=8))}@{random.choice(domains)}"

# Database connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="BRATmusic"
)

cursor = db.cursor()

# Function to generate random email
def random_email():
    domains = ["example.com", "music.com", "artistmail.com", "mail.com"]
    return f"{''.join(random.choices(string.ascii_letters + string.digits, k=8))}@{random.choice(domains)}"

# Full path to the Excel file
excel_file = 'userINFO.xlsx'

# Read Excel file
df = pd.read_excel(excel_file)

# Ensure the column 'names' exists
if 'names' not in df.columns:
    raise ValueError("The Excel file must have a column named 'names'.")

# Drop rows where 'names' is NaN
df = df.dropna(subset=['names'])

# Remove duplicates
df = df.drop_duplicates(subset=['names'])

# Add the 'artistEmail' column with random emails
df['artistEmail'] = [random_email() for _ in range(len(df))]

# Save updated DataFrame back to the Excel file
df.to_excel(excel_file, index=False)
print(f"Updated {excel_file} with a new column 'artistEmail'.")

# Check for missing values in the new columns
if df['artistName'].isnull().any() or df['artistEmail'].isnull().any():
    print("Missing values detected in 'artistName' or 'artistEmail'. Please check your Excel file.")
    exit()

# Function to insert data into the database
def populate_artist_table(names, emails):
    for name, email in zip(names, emails):
        # Check if the name already exists in the database
        cursor.execute(
            "SELECT COUNT(*) FROM Artist WHERE artistName = %s", (name,))
        if cursor.fetchone()[0] > 0:
            print(f"Skipping duplicate: {name}")
            continue

        # Generate other data fields
        total_duration = random.randint(10000, 1000000)  # Random total duration
        revenue_generated = round(random.uniform(50000, 2000000), 2)  # Random revenue
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))  # Random password

        # SQL query
        sql = "INSERT INTO Artist (artistName, totalDurationListenedTo, revenueGenerated, email, password) VALUES (%s, %s, %s, %s, %s)"
        values = (name, total_duration, revenue_generated, email, password)

        # Execute query
        cursor.execute(sql, values)

    # Commit the changes
    db.commit()
    print(f"{len(names)} rows processed (duplicates skipped).")


# Call the function with names and emails
populate_artist_table(df['artistName'].tolist(), df['artistEmail'].tolist())

# Close the connection
cursor.close()
db.close()
