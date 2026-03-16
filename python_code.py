comedy_movies = ["anaconda","grown ups 1","grown ups 2","22 jumpstreet"]
action_movies =["gladiator 1", "gladiator 2", "maze runner","the working man"]
horror_movies = ["annabelle comes homes", "get out", "US", "conjuring"]
Sci_fi_movies = ["predator badlands","avengers endgame","hunger games part 1 mockingbird","hunger games part 2 mocking bird"]
thriller_movies = [" after the hunt", "prisoners","incpetion", "carry on"]
action_tickets_available = [0,0,0,0,0]
horror_tickets_available = [0,0,0,0,0]
sci_fi_tickets_available = [0,0,0,0,0]
thriller_tickets_available=[0,0,0,0,0]
comedy_tickets_available = [0,0,0,0,0]
TICKET_PRICE = 8.00
while True:
    name = input("Enter a name: ")
    while True:
        genre = input("Enter your genre for movie selections (comedy, action, horror, sci-fi, thriller): ").lower()
        if genre in ["comedy","action","horror", "sci-fi", "thriller"]:
            break
        else:
            print("Invalid genre. Please try again.")
    num_tickets = int(input("enter the number of tickets that want you want to purchase:"))
    while num_tickets <=0 or num_tickets > 200:
        num_tickets = int(input("please reenter the number of tickets that want you want to purchase:"))
        tickets_available = tickets_available - num_tickets 
    cost_price = num_tickets * TICKET_PRICE
if genre == "comedy":
        movie_selection = input("please select your preffered movie from the genre 0 for anaconda,1 for grown ups 1 , 2 for grown ups 2  and 3 22 jumpstreet")
        print(f"Thank you for selecting {comedy_movies[movie_selection]}, the price is {cost_price:.2f}")    
elif genre == "action":
        movie_selection = input("please select your preffered movie from the genre")
        print(f"thank you for selecting the movie {action_movies[movie_selection]}, the price is {cost_price:.2f} ") 
elif genre == "sci_fi":
        movie_selection = int(input("please select your preffered movie from the genre 0 for predator badlands,1 for avengers endgame , 2 for  hunger games part 1 mockingbird   and 3 for  hunger games part 2 mockingbird"))
        print(f"Thank you for selecting {Sci_fi_movies[movie_selection]}, the price is {cost_price:.2f}")
elif genre == "horror": 
        movie_selection = int(input("please select your preffered movie from the genre 0 for annabelle comes homes,1 for get out , 2 for US and 3 for conjuring"))
        print(f"Thank you for selecting {horror_movies[movie_selection]}, the price is {cost_price:.2f} ")
elif genre == "thriller":  
        movie_selection = int(input("please select your preffered movie from the genre 0 for after the hunt,1 for  prisoners, 2 for inception, 3 for carry on"))
        print(f"Thank you for selecting {thriller_movies[movie_selection]}, the price is {cost_price:.2f} ")
again = input("do you want to make another booking (yes/no):")
if again !="yes":
    break