import sqlite3

def get_table_names(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    
    # SQL query to get the list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    # Fetch all the results
    tables = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    # Return the list of table names (extracted from tuples)
    return [table[0] for table in tables]

# Example usage:
db_path = r'C:\Users\Jayanth C\AppData\Roaming\DeidentificationTool\hj\TablesData\Data.db'  # Specify your SQLite database path
table_names = get_table_names(db_path)
print("List of tables:", table_names)
