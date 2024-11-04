import sqlite3

# Connect to the SQLite database (replace 'your_database.db' with your database file)
conn = sqlite3.connect(r'C:\Users\Jayanth C\AppData\Roaming\DeidentificationTool\nnn\TablesData\Data.db')

# Cursor object to execute queries
cursor = conn.cursor()

# Define the table name (replace 'your_table' with the actual table name)
table_name = 'de_identified_SpreedSheet'

# Query to get column information of the table
cursor.execute(f"PRAGMA table_info({table_name});")

# Fetch all results
columns_info = cursor.fetchall()

# Close the connection
conn.close()

# Display column names and their data types
for column in columns_info:
    column_id = column[0]          # Column ID (index position)
    column_name = column[1]        # Column name
    column_type = column[2]        # Column data type

    print(f"Column: {column_name}, Data Type: {column_type}")
