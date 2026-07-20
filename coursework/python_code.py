import sqlite3
conn = sqlite3.connect("cinema.db")
cursor = conn.cursor()
comedy_tickets =[0,0,0,0]
action_tickets =[0,0,0,0]
horror_tickets =[0,0,0,0]
sci_fi_tickets =[0,0,0,0]
thriller_tickets = [0,0,0,0]
TICKET_PRICE = 10.99
max_tickets = 100
sold_tickets = 0
tickets_available = 100
def sign_up():
    while True:

        username = input("Enter a username: ")
        password = input("Enter a password: ")
        confirm_password = input("Confirm your password: ")

        if username == "" or password == "":
            print("Please complete all fields.\n")
            continue

        
        if password != confirm_password:
            print("Passwords do not match.\n")
            continue

      
        cursor.execute(
            "SELECT * FROM Customers WHERE username = ?",
            (username,)
        )

        if cursor.fetchone():
            print("Username already exists.\n")
            continue

        
        cursor.execute(
            "INSERT INTO Customers (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()

        print("Account created successfully!")
        break
# sign_up()
def log_in():
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        cursor.execute(
            "SELECT * FROM Customers WHERE username = ? AND password = ?",
            (username, password)
        )

        if cursor.fetchone():
            print("Login successful!")
            return username
        else:
            print("Invalid username or password. Please try again.\n")


def choose_movie(username):
    while True:
        genre = input("Enter genre (comedy, action, horror, sci-fi, thriller): ").lower()

        if genre in ["comedy", "action", "horror", "sci-fi", "thriller"]:
            break
        else:
            print("Invalid genre. Try again.")

    cursor.execute("""
        SELECT Title, Genre, AgeRating, Duration, Description, FilmID
        FROM Films
        WHERE Genre = ?
    """, (genre.title(),))
     
    movies = cursor.fetchall()
    
    for i, movie in enumerate(movies):
        print()
        print("Movie number:", i)
        print("Title:", movie[0])
        print("Genre:", movie[1])
        print("Rating:", movie[2])
        print("Duration:", movie[3], "minutes")
        print("Description:", movie[4])

    while True:
        try:
            movie_selection = int(input("Select movie number: "))

            if 0 <= movie_selection < len(movies):
                break

            print("Invalid selection.")

        except ValueError:
            print("Please enter a number.")

    selected_movie = movies[movie_selection][0]
    film_id = movies[movie_selection][5]

    movie = selected_movie
    print(f"Thank you {username} for selecting {selected_movie}.")
    return film_id
logged_in_user = log_in()
movie_id = choose_movie(logged_in_user)
print(movie_id)
def choose_screening(movie_id):

    cursor.execute("""
        SELECT ScreeningID, ScreeningDate, ScreeningTime, ScreenNumber
        FROM Screenings
        WHERE FilmID = ?
    """, (movie_id,))

    screenings = cursor.fetchall()

    if len(screenings) == 0:
        print("No screenings available.")
        return None

    for i, screenings in enumerate(screenings):
        print(f"\n{i}")
        print("Date:", screenings[1])
        print("Time:", screenings[2])
        print("Screen:", screenings[3])

    while True:
        try:
            choice = int(input("Select a screening: "))

            if 0 <= choice < len(screenings):
                return screenings[choice][0]
            

            print("Invalid selection.")

        except ValueError:
            print("Please enter a number.")
screen_id = choose_screening(movie_id)
def choose_seat(screen_id):

    while True:

        cursor.execute("""
            SELECT seatID, seatnumber, isavailable
            FROM Seats
            WHERE screeningID = ?
        """, (screen_id,))

        seats = cursor.fetchall()

        print("\nAvailable seats")

        for seat in seats:
            if seat[2]:
                print(seat[1], "- Available")
            else:
                print(seat[1], "- Booked")

        seat_choice = input("\nChoose a seat: ").upper()

        cursor.execute("""
            SELECT seatID, isavailable
            FROM Seats
            WHERE screeningID = ?
            AND seatnumber = ?
        """, (screen_id, seat_choice))

        seat = cursor.fetchone()

        if seat is None:
            print("Seat does not exist.")
            continue

        if seat[1] == False:
            print("That seat is already booked.")
            continue

        confirm = input("Confirm booking? (Y/N): ").upper()

        if confirm == "Y":

            cursor.execute("""
                UPDATE Seats
                SET isavailable = FALSE
                WHERE seatID = ?
            """, (seat[0],))

            conn.commit()

            print("Booking successful!")

            return seat[0]

        print("Booking cancelled.")
choose_seat(screen_id)

    # for row in range(10):
    #    for col in range(10):
    #        [row][col] = 0
    # while True:
    #     num_tickets = int(input("Enter number of tickets: "))
    #     sold_tickets = sold_tickets + num_tickets
    #     print(sold_tickets)
    #     if 0 < num_tickets < (max_tickets - sold_tickets):
    #         break
    #     else:
    #         print("Not enough tickets available or invalid.")
    # cost_price = num_tickets * TICKET_PRICE
    # if genre == "comedy":
    #     print(comedy_movies)
    #     while True:
    #         movie_selection = int(input("Select movie (0-3): "))
    #         if 0 <= movie_selection < 4:
    #             break
    #         print("Invalid selection.")
    #     comedy_tickets[movie_selection] = comedy_tickets[movie_selection] + num_tickets
    #     tickets_available = max_tickets - sold_tickets
    #     print(f"Thank you {name} for selecting {comedy_movies[movie_selection]}, total price is £{cost_price:.2f}")
    # elif genre == "action":
    #     print(action_movies)
    #     while True:
    #         movie_selection = int(input("Select movie (0-3): "))
    #         if 0 <= movie_selection < 4:
    #             break
    #         print("Invalid selection.")
    #     action_tickets[movie_selection] = action_tickets[movie_selection] + num_tickets
    #     tickets_available = max_tickets - sold_tickets
    #     print(f"Thank you {name} for selecting {action_movies[movie_selection]}, total price is £{cost_price:.2f}")
    # elif genre == "horror":
    #     print(horror_movies)
    #     while True:
    #         movie_selection = int(input("Select movie (0-3):"))
    #         if 0 <= movie_selection < 4:
    #             break
    #         print("Invalid selection.")
    #     horror_tickets[movie_selection] = horror_tickets[movie_selection] + num_tickets
    #     tickets_available = max_tickets - sold_tickets
    #     print(f"Thank you {name} for selecting {horror_movies[movie_selection]}, total price is £{cost_price:.2f}")
    # elif genre == "sci-fi":
    #     print(sci_fi_movies)
    #     while True:
    #         movie_selection = int(input("Select movie (0-3): "))
    #         if 0 <= movie_selection < 4:
    #             break
    #         print("Invalid selection.")
    #     sci_fi_tickets[movie_selection] = sci_fi_tickets[movie_selection] + num_tickets
    #     tickets_available = max_tickets - sold_tickets
    #     print(f"Thank you {name} for selecting {sci_fi_movies[movie_selection]}, total price is £{cost_price:.2f}")
    # elif genre == "thriller":
    #     print(thriller_movies)
    #     while True:
    #         movie_selection = int(input("Select movie (0-3): "))
    #         if 0 <= movie_selection < 4:
    #             break
    #         print("Invalid selection.")
    #     thriller_tickets[movie_selection] = thriller_tickets[movie_selection] + num_tickets
    #     tickets_available = max_tickets - sold_tickets
    #     print(f"Thank you {name} for selecting {thriller_movies[movie_selection]}, total price is £{cost_price:.2f}")
    #     print(tickets_available)
    # if tickets_available == 0:
    #     print("There are no more tickets available")
    #     break
    # else:
    #     print("There are", tickets_available, "tickets available")