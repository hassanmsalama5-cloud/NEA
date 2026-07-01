import sqlite3
conn = sqlite3.connect("cinema.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()
conn.close()