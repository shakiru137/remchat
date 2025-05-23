import mysql.connector
import os

def get_db_connection():
    """
    Establishes a connection to the MySQL database.

    This function attempts to connect to the specified MySQL database and 
    returns the connection object if successful. In case of a connection 
    error, it logs the error and returns None.

    Returns:
        mysql.connector.connection.MySQLConnection or None: 
        The database connection object if successful, otherwise None.
    """
    try:
        conn = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', 'oluwasegun137'),
            database=os.environ.get('DB_NAME', 'remgram2')
        )
        if conn.is_connected():
            return conn
        else:
            print("Failed to connect to the database.")
            return None
    except mysql.connector.Error as err:
        print(f"Database connection error: {err} 😒")
        return None
