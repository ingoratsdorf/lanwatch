import sqlite3
from typing import List
from dataclasses import dataclass
from threading import Lock

# Assuming models.Host is a dataclass in Python
@dataclass
class Host:
    # Add all the fields from models.Host here
    # Example fields (replace with actual fields from models.Host):
    date: str
    # ... other fields ...

# Global lock for thread safety
mu = Lock()

def connect_db() -> sqlite3.Connection:
    """Connect to the SQLite database."""
    # Assuming SQLite database connection
    # Replace with actual connection logic from your Go code
    conn = sqlite3.connect('your_database.db')
    return conn

def db_exec(sql_statement: str) -> None:
    """Execute a SQL statement."""
    try:
        db = connect_db()
        with db:
            with mu:
                cursor = db.cursor()
                cursor.execute(sql_statement)
    except Exception as e:
        # Equivalent to check.IfError(err)
        print(f"Database error: {e}")
        raise
    finally:
        db.close()

def select(table: str) -> List[Host]:
    """Get all hosts from the specified table, ordered by date descending."""
    sql_statement = f'SELECT * FROM {table} ORDER BY "DATE" DESC'
    db_hosts = []

    try:
        db = connect_db()
        with db:
            with mu:
                cursor = db.cursor()
                cursor.execute(sql_statement)
                rows = cursor.fetchall()
                
                # Convert rows to Host objects
                # This assumes rows are in the same order as Host fields
                db_hosts = [Host(*row) for row in rows]
    except Exception as e:
        print(f"Database error: {e}")
        raise
    finally:
        db.close()

    return db_hosts
