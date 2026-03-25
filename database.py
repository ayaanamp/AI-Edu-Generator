import sqlite3

conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_text TEXT,
    output TEXT
)
""")

conn.commit()

def save_data(input_text, output):
    cursor.execute(
        "INSERT INTO quiz_history (input_text, output) VALUES (?, ?)",
        (input_text, output)
    )
    conn.commit()