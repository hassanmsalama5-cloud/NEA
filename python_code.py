comedy_movies = ["anaconda","grown ups 1","grown ups 2","22 jumpstreet"]
action_movies = ["gladiator 1", "gladiator 2", "maze runner","the working man"]
horror_movies = ["annabelle comes home", "get out", "US", "conjuring"]
sci_fi_movies = ["predator badlands","avengers endgame","hunger games part 1 mockingbird","hunger games part 2 mocking bird"]
thriller_movies = ["after the hunt", "prisoners","inception", "carry on"]
comedy_tickets =[0,0,0,0]
action_tickets =[0,0,0,0]
horror_tickets =[0,0,0,0]
sci_fi_tickets =[0,0,0,0]
thriller_tickets=[0,0,0,0]
TICKET_PRICE = 8.00
max_tickets = 200
sold_tickets = 0
total_sold = 0
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
    while True:
        num_tickets = int(input("Enter number of tickets: "))
        if 0 < num_tickets <= (max_tickets - sold_tickets):
            break
        else:
            print("Not enough tickets available or invalid.")
    cost_price = num_tickets * TICKET_PRICE
    sold_tickets == num_tickets
    print(sold_tickets)
    if genre == "comedy":
        print(comedy_movies)
        while True:
            movie_selection = int(input("Select movie (0-3): "))
            if 0 <= movie_selection < 4:
                break
            print("Invalid selection.")
        comedy_tickets[movie_selection] +  num_tickets  == comedy_tickets[movie_selection] 
        total_sold = total_sold + sold_tickets
        print(f"Thank you {name} for selecting {comedy_movies[movie_selection]}, total price is £{cost_price:.2f}")
    elif genre == "action":
        print(action_movies)
        while True:
            movie_selection = int(input("Select movie (0-3): "))
            if 0 <= movie_selection < 4:
                break
            print("Invalid selection.")
        action_tickets[movie_selection] + num_tickets == action_tickets[movie_selection]
        total_sold = total_sold + sold_tickets
        print(f"Thank you {name} for selecting {action_movies[movie_selection]}, total price is £{cost_price:.2f}")
    elif genre == "horror":
        print(horror_movies)
        while True:
            movie_selection = int(input("Select movie (0-3):"))
            if 0 <= movie_selection < 4:
                break
            print("Invalid selection.")
        horror_tickets[movie_selection] + num_tickets ==  horror_tickets[movie_selection]
        total_sold = total_sold + sold_tickets
        print(f"Thank you {name} for selecting {horror_movies[movie_selection]}, total price is £{cost_price:.2f}")
    elif genre == "sci-fi":
        print(sci_fi_movies)
        while True:
            movie_selection = int(input("Select movie (0-3): "))
            if 0 <= movie_selection < 4:
                break
            print("Invalid selection.")
        sci_fi_tickets[movie_selection] + num_tickets == sci_fi_tickets[movie_selection]
        total_sold = total_sold + sold_tickets
        print(f"Thank you {name} for selecting {sci_fi_movies[movie_selection]}, total price is £{cost_price:.2f}")
    elif genre == "thriller":
        print(thriller_movies)
        while True:
            movie_selection = int(input("Select movie (0-3): "))
            if 0 <= movie_selection < 4:
                break
            print("Invalid selection.")
        thriller_tickets[movie_selection] + num_tickets == thriller_tickets[movie_selection]
        total_sold = total_sold + sold_tickets
        print(f"Thank you {name} for selecting {thriller_movies[movie_selection]}, total price is £{cost_price:.2f}")
        tickets_available = max_tickets - total_sold
        print(tickets_available)
    if tickets_available == 0:
        print("There are no more tickets available")
        break
    else:
        print("There are", tickets_available, "tickets available")