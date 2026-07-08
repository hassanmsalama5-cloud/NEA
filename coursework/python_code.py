import sqlite3
conn = sqlite3.connect("cinema.db")
cursor = conn.cursor()
comedy_tickets =[0,0,0,0]



action_tickets =[0,0,0,0]
horror_tickets =[0,0,0,0]
sci_fi_tickets =[0,0,0,0]
thriller_tickets = [0,0,0,0]
TICKET_PRICE = 8.00
max_tickets = 200
sold_tickets = 0
tickets_available = 200
while True:
    name = input("Enter your name (or type 'exit' to quit): ")
    if name == "exit":
        break
    while True:
        genre = input("Enter genre (comedy, action, horror, sci-fi, thriller): ").lower()
        if genre in ["comedy","action","horror","sci-fi","thriller"]:
            break
        else:
            print("Invalid genre. Try again.")
    cursor.execute("""
    SELECT Title, Genre, AgeRating, Duration, Description
    FROM Films
    WHERE Genre = ?
    """, (genre.title(),))
    movies = cursor.fetchall()
    for i, movie in enumerate(movies):
        print()
        print("The movie number is", i)
        print("Title:", movie[0])
        print("Genre:", movie[1])
        print("Rating:", movie[2])
        print("Duration:", movie[3], "minutes")
        print("Description:", movie[4])
    while True:
        movie_selection = int(input("Select movie number from (0 to 3 ): "))
        if 0 <= movie_selection < len(movies):
            break
        print("Invalid selection.")
    selected_movie = movies[movie_selection][0]
    print(f"Thank you {name} for selecting {selected_movie}.")


    # for row in range(20):
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
    cost_price = num_tickets * TICKET_PRICE
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