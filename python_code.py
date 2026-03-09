import random
Movie_array = ["anaconda ", "gladiator 2", "Annabelle comes home", "predator badlands","After the hunt"]
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
    cost_price = num_tickets * TICKET_PRICE
    if genre == "comedy":
        movie_confirming = input(f"Is your movie selection'{Movie_array[0]}'? (yes/no): ").lower() 
        if movie_confirming =="yes": 
            print(f"Thank you for confirming, the price is {cost_price:.2f}")
            for i in range(num_tickets):
                seat_number = random.randint(1, 200)
                print ("your seat number is ", seat_number)
        else:
            print("You did not confirm the comedy movie selection.") 
    elif genre == "action":
        movie_confirming = input(f"Is your movie selection '{Movie_array[1]}'? (yes/no): ").lower() 
        if movie_confirming =="yes": 
            print(f"Thank you for confirming, the price is {cost_price:.2f} ")
            for i in range(num_tickets):
                seat_number = random.randint(1, 200)
                print ("your seat number is ", seat_number) 
        else: 
            print("You did not confirm the action movie selection.") 
    elif genre == "sci-fi":
        movie_confirming = input(f"Is your movie selection '{Movie_array[2]}'? (yes/no): ").lower() 
        if movie_confirming =="yes": 
         print(f"Thank you for confirming, the price is {cost_price:.2f}")
         for i in range(num_tickets):
                seat_number = random.randint(1, 200)
                print ("your seat number is ", seat_number)  
        else: 
            print("You did not confirm the sci-fi movie selection.") 
    elif genre == "horror": 
        movie_confirming = input(f"Is your movie selection '{Movie_array[3]}'? (yes/no): ").lower() 
        if movie_confirming =="yes": 
            print(f"Thank you for confirming, the price is {cost_price:.2f} ")
            for i in range(num_tickets):
                seat_number = random.randint(1, 200)
                print ("your seat number is", seat_number) 
        else: 
            print("You did not confirm the horror movie selection.") 
    elif genre == "thriller":
        movie_confirming = input(f"Is your movie selection '{Movie_array[4]}'? (yes/no): ").lower() 
        if movie_confirming =="yes": 
            print(f"Thank you for confirming, the price is {cost_price:.2f} ")
            for i in range(num_tickets):
                seat_number = random.randint(1, 200)
                print ("your seat number is", seat_number) 
        else: 
            print("You did not confirm the thriller movie selection.")
    again = input("do you want to make another booking (yes/no):")
    if again !="yes":
        break

