import sqlite3
conn = sqlite3.connect("cinema.db")
cursor = conn.cursor()
cursor.execute("""
INSERT INTO films (Title, Genre, Duration, AgeRating, Description) VALUES   (?, ?, ?, ?, ?)          
""", ('Inception', 'Sci-Fi', 148, 'PG-13', 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.'))
cursor.execute("DELETE FROM films WHERE Title = ?", ('Inception',))
cursor.execute(
    "UPDATE Customers SET password = ? WHERE CustomerID = ?",
    ("123456", 1)
)

conn.commit()
conn.close()