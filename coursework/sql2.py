
import logging
import sqlite3

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

connection = None

try:
    connection = sqlite3.connect("cinema.db")
    cursor = connection.cursor()

    # Use only a trusted, hard-coded table name.
    table_name = "bookings"

    cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')
    connection.commit()

    print(f"Table '{table_name}' dropped successfully.")

except sqlite3.Error as error:
    logging.exception("SQL error while dropping the table: %s", error)

    if connection:
        connection.rollback()

finally:
    if connection:
        connection.close()