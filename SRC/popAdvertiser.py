import pandas as pd
import mysql.connector

# Database connection details
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="BRATmusic"
)

# Path to the Excel file
excel_file = r'\advertiser_data.xlsx'

try:
    # Load the data into a DataFrame
    df = pd.read_excel(excel_file)

    # Ensure the column "Company" exists
    if "Company" not in df.columns:
        raise ValueError("The Excel file must have a 'Company' column.")

    # Remove duplicates and NaN values from the DataFrame
    df = df.dropna(subset=["Company"]).drop_duplicates(subset=["Company"])

    # Create a cursor object
    cursor = db.cursor()

    # Insert data into the Advertiser table
    for _, row in df.iterrows():
        company_name = row['Company']

        # Use a parameterized query to prevent SQL injection
        sql = "INSERT IGNORE INTO Advertiser (company) VALUES (%s)"  # IGNORE avoids duplicate entries
        cursor.execute(sql, (company_name,))

    # Commit changes
    db.commit()
    print(f"Advertiser data from '{excel_file}' has been successfully inserted into the database.")

except FileNotFoundError:
    print(f"Error: The file '{excel_file}' was not found.")
except ValueError as ve:
    print(f"Error: {ve}")
except pymysql.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # Ensure the database connection is closed
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'db' in locals() and db:
        db.close()
