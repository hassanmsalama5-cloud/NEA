import sqlite3
conn = sqlite3.connect("cinema.db")
cursor = conn.cursor()
def admin_sign_up():

    username = input("New username: ")
    password = input("New password: ")

    cursor.execute("""
        INSERT INTO Admins (username, password)
        VALUES (?, ?)
    """, (username, password))

    conn.commit()

    print("Administrator added.")
# admin_sign_up()
def admin_login():
    while True:
        username = input("Enter your admin username: ")
        password = input("Enter your admin password: ")

        cursor.execute(
            "SELECT * FROM Admins WHERE username = ? AND password = ?",
            (username, password)
        )

        admin = cursor.fetchone()

        if admin:
            print("Admin login successful!")
            admin_id = admin[0]
            return admin_id 
        print("Invalid admin credentials. Please try again.\n")
admin_id = admin_login()
def add_film():
    title = input("Enter film title: ")
    genre = input("Enter film genre: ")
    duration = input("Enter film duration (in minutes): ")
    description = input("Enter film description: ")
    age_rating = input("Enter film age rating: ")

    cursor.execute("""
        INSERT INTO films (Title, Genre, Duration, Description, AgeRating)
        VALUES (?, ?, ?, ?, ?)
    """, (title, genre, duration, description, age_rating))

    conn.commit()

    print("Film added successfully.")

def add_screening():
    film_id = input("Enter the ID of the film for the screening: ")
    screening_date = input("Enter the screening date (YYYY-MM-DD): ")
    screening_time = input("Enter the screening time (HH:MM): ")
    screen_number = input("Enter the screen number: ")

    cursor.execute("""
        INSERT INTO Screenings (FilmID, ScreeningDate, ScreeningTime, ScreenNumber)
        VALUES (?, ?, ?, ?)
    """, (film_id, screening_date, screening_time, screen_number))

    conn.commit()

    print("Screening added successfully.")

def remove_film():
    while True:
        try:
            film_id = int(input("Enter the ID of the film to remove: "))    
        except ValueError:
            print("Please enter a valid film ID.")
            continue

    cursor.execute("""
        DELETE FROM films WHERE FilmID = ?
    """, (film_id,))

    conn.commit()

    print("Film removed successfully.")

def remove_screening():
    while True:
        try:
            screening_id = int(input("Enter the ID of the screening to remove: "))

            cursor.execute("""
                DELETE FROM Screenings WHERE ScreeningID = ?
            """, (screening_id,))
            break

        except ValueError:
            print("Please enter a valid screening ID.")

    conn.commit()

    print("Screening removed successfully.")

def edit_film():
        film_id = int(input("Enter the ID of the film to edit: "))
        new_title = input("Enter the new title: ")
        new_genre = input("Enter the new genre: ")
        new_duration = input("Enter the new duration:")
        new_description = input("Enter the new description:")
        new_age_rating = input("Enter the new age rating: ")

        cursor.execute("""
            UPDATE films
            SET Title = ?, Genre = ?, Duration = ?, Description = ?, AgeRating = ?
            WHERE FilmID = ?
    """, (new_title, new_genre, new_duration, new_description, new_age_rating, film_id))

        conn.commit()

        print("Film updated successfully.")

def edit_screening():
    screening_id = int(input("Enter the ID of the screening to edit: "))      
    new_film_id = input("Enter the new film ID: ")
    new_screening_date = input("Enter the new screening date: ")
    new_screening_time = input("Enter the new screening time: ")
    new_screen_number = input("Enter the new screen number: ")

    cursor.execute("""
        UPDATE Screenings
        SET FilmID = ?, ScreeningDate = ?, ScreeningTime = ?, ScreenNumber = ?
        WHERE ScreeningID = ?
    """, (new_film_id, new_screening_date, new_screening_time, new_screen_number, screening_id))

    conn.commit()

    print("Screening updated successfully.")

def administrator_menu():
    while True:

        print("""
1. Add Film
2. Add Screening
3. Remove Screening
4. Remove Film
5. Edit Film
6. Edit Screening
7. Logout
""")

        choice = input("Choice: ")

        if choice == "1":
            add_film()

        elif choice == "2":
            add_screening()

        elif choice == "3":
            remove_screening()

        elif choice == "4":
            remove_film()

        elif choice == "5":
            edit_film()

        elif choice == "6":
            edit_screening()

        elif choice == "7":
            print("Logging out...")
            break
administrator_menu()
