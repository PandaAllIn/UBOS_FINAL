"""Verifies the content of the Manifold metrics database."""

import sqlite3

DB_FILE = "/srv/janus/02_FORGE/src/manifold/manifold_metrics.db"

def verify_db_contents():
    """Connects to the DB, reads all metrics, and prints them."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        print(f"--- Querying all records from {DB_FILE} ---")
        cursor.execute("SELECT * FROM metrics ORDER BY timestamp DESC;")
        
        rows = cursor.fetchall()
        
        if not rows:
            print("Database is empty.")
            return

        for row in rows:
            print(row)
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    verify_db_contents()
