import pandas as pd
import pymysql

# Database connection details
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "sarah070920",
    "database": "BRATmusic"
}

# Read the Excel file
excel_file = "advertiser_data.xlsx"

try:
    # Load the data into a DataFrame
    df = pd.read_excel(excel_file)

    # Ensure the column "Company" exists
    if "Company" not in df.columns:
        raise ValueError("The Excel file must have a 'Company' column.")

    # Connect to the database
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Insert data into the Advertiser table
    for _, row in df.iterrows():
        company_name = row['Company']
        # Use a parameterized query
        sql = "INSERT INTO Advertiser(company) VALUES (%s)"
        cursor.execute(sql, (company_name,))

    # Commit changes and close the connection
    conn.commit()
    print(
        f"Advertiser data from '{excel_file}' has been successfully inserted into the database.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure the database connection is closed
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn:
        conn.close()
