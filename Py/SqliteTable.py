import sqlite3
import pandas as pd

# Establish connection to the SQLite database
conn = sqlite3.connect(r'C:\Users\Jayanth C\AppData\Roaming\DeidentificationTool\Config\TablesData\Data.db')

# Write the SQL query to select the table
query = "SELECT * FROM de_identified_hierarchy"

# Read the table into a pandas DataFrame
df = pd.read_sql_query(query, conn)

# Print the DataFrame
print(df)

# Close the database connection
conn.close()
