import sqlite3

conn = sqlite3.connect("rover_memory.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_name TEXT,
    event_type TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


def save_event(object_name, event_type):
    cursor.execute(
        """
        INSERT INTO events (object_name, event_type)
        VALUES (?, ?)
        """,
        (object_name, event_type)
    )
    conn.commit()


def get_recent_events():
    cursor.execute("""
        SELECT object_name, event_type, timestamp
        FROM events
        ORDER BY id DESC
        LIMIT 50
    """)

    return cursor.fetchall()