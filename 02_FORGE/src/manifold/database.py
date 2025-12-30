"""Initializes the database for storing Pattern Engine metrics over time."""

import sqlite3

DB_FILE = "/srv/janus/02_FORGE/src/manifold/manifold_metrics.db"


def initialize_db():
    """Creates the metrics table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        timestamp INTEGER PRIMARY KEY,
        entropy_index REAL NOT NULL,
        resonance_density REAL NOT NULL,
        cohesion_flux REAL NOT NULL,
        signal_integrity REAL NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_FILE}")

if __name__ == "__main__":
    initialize_db()
