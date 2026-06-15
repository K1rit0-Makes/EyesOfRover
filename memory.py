import sqlite3

DB_NAME = "rover_memory.db"


def initialize_database():

    conn = sqlite3.connect(DB_NAME)

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

    conn.close()


def save_event(
    object_name,
    event_type
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO events
        (
            object_name,
            event_type
        )
        VALUES (?, ?)
        """,
        (
            object_name,
            event_type
        )
    )

    conn.commit()

    conn.close()


def get_recent_events():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        object_name,
        event_type,
        timestamp
    FROM events
    ORDER BY id DESC
    LIMIT 50
    """)

    data = cursor.fetchall()

    conn.close()

    return data


initialize_database()