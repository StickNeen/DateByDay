import random
from datetime import datetime, timedelta

def generate_random_date():
    # Generate a random date between years 1900 and 2100
    rangeweight = random.randint(1,4)
    if rangeweight <= 3:
    	start_date = datetime(1900, 1, 1)
    	end_date = datetime(2099, 12, 31)
    else:
    	start_date = datetime(1700, 1, 1)
    	end_date = datetime(2499, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)
    return random_date

def get_user_guess():
    return input("Guess the day of the week (e.g., Monday, Tuesday, etc.): ").strip().capitalize()

def main():
    while True:
        random_date = generate_random_date()
        correct_day = random_date.strftime("%A")
        
        print(f"\nRandom Date (YYYY-MM-DD): {random_date.strftime('%Y-%m-%d')}")

        while True:
            user_guess = get_user_guess()
            if user_guess == correct_day:
                print("Correct! Well done.")
                break
            else:
                print("Incorrect. Try again.")
        
        play_again = input("Would you like to guess another date? ([y]es/[n]o): ").strip().lower()
        if play_again != 'y' and play_again != 'yes':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
