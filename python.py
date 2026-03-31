# Cinema Ticket Booking System - Fixed Version
comedy_movies = ["Anaconda", "Grown Ups 1", "Grown Ups 2", "22 Jump Street"]
action_movies = ["Gladiator 1", "Gladiator 2", "Maze Runner", "The Working Man"]
horror_movies = ["Annabelle Comes Home", "Get Out", "Us", "The Conjuring"]
sci_fi_movies = ["Predator Badlands", "Avengers Endgame", 
                 "Hunger Games: Mockingjay Part 1", "Hunger Games: Mockingjay Part 2"]
thriller_movies = ["After the Hunt", "Prisoners", "Inception", "Carry On"]

# Ticket counters - these will increase when people book
comedy_tickets = [0, 0, 0, 0]
action_tickets = [0, 0, 0, 0]
horror_tickets = [0, 0, 0, 0]
sci_fi_tickets = [0, 0, 0, 0]
thriller_tickets = [0, 0, 0, 0]

TICKET_PRICE = 8.00
MAX_TICKETS = 200
total_sold = 0

print("Welcome to the Cinema Ticket Booking System\n")

while total_sold < MAX_TICKETS:
    name = input("Enter your name (or type 'exit' to quit): ").strip()
    if name.lower() == "exit":
        break

    # Genre selection
    while True:
        genre = input("Enter genre (comedy, action, horror, sci-fi, thriller): ").lower().strip()
        if genre in ["comedy", "action", "horror", "sci-fi", "thriller"]:
            break
        print("Invalid genre. Try again.")

    # Number of tickets
    while True:
        try:
            num_tickets = int(input("Enter number of tickets: "))
            if num_tickets < 1:
                print("Must buy at least 1 ticket.")
            elif total_sold + num_tickets > MAX_TICKETS:
                print(f"Only {MAX_TICKETS - total_sold} tickets left!")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")

    cost_price = num_tickets * TICKET_PRICE

    # Choose movie and update correct ticket list
    if genre == "comedy":
        movie_list = comedy_movies
        ticket_list = comedy_tickets
    elif genre == "action":
        movie_list = action_movies
        ticket_list = action_tickets
    elif genre == "horror":
        movie_list = horror_movies
        ticket_list = horror_tickets
    elif genre == "sci-fi":
        movie_list = sci_fi_movies
        ticket_list = sci_fi_tickets
    else:  # thriller
        movie_list = thriller_movies
        ticket_list = thriller_tickets

    print("\nAvailable movies:")
    for i in range(4):
        print(f"{i}: {movie_list[i]}")

    while True:
        try:
            movie_selection = int(input(f"Select movie (0-3): "))
            if 0 <= movie_selection < 4:
                break
            print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")

    # === THIS IS THE IMPORTANT LINE ===
    # It increases the ticket count for the chosen movie
    ticket_list[movie_selection] += num_tickets

    total_sold += num_tickets

    # Receipt
    print(f"\nThank you {name}!")
    print(f"You selected: {movie_list[movie_selection]}")
    print(f"Tickets booked: {num_tickets}")
    print(f"Total price: £{cost_price:.2f}")

    # === SHOW THAT TICKETS ARE INCREASING ===
    print("\n" + "="*55)
    print("UPDATED TICKET COUNTS")
    print("="*55)
    print(f"{genre.capitalize()} section:")
    for i in range(4):
        print(f"  Movie {i}: {movie_list[i]}  →  {ticket_list[i]} tickets sold")
    print(f"\nTotal tickets sold overall: {total_sold} / {MAX_TICKETS}")
    print("="*55)

    # Check if sold out
    tickets_available = MAX_TICKETS - total_sold
    if tickets_available == 0:
        print("\nSORRY! All tickets have been sold out.")
        break
    else:
        print(f"\n{tickets_available} tickets still available.\n")

# Final summary when program ends
print("\n" + "="*60)
print("BOOKING SESSION FINISHED")
print(f"Total tickets sold: {total_sold}")
print("\nFinal ticket counts:")
print("Comedy   :", sum(comedy_tickets))
print("Action   :", sum(action_tickets))
print("Horror   :", sum(horror_tickets))
print("Sci-Fi   :", sum(sci_fi_tickets))
print("Thriller :", sum(thriller_tickets))
print("="*60)