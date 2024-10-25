import random

def generate_number():
    # Create a weighted choice to make multiples of 12 more likely
    if random.random() < 0.4:  # 40% chance of generating a multiple of 12
        return random.choice([i for i in range(12, 101, 12)])
    else:
        return random.randint(1, 100)

def check_answer(number, user_input):
    if number % 12 == 0:
        correct_answer = number // 12
        if user_input == str(correct_answer):
            print("Correct!")
        else:
            print(f"Incorrect. The answer was {correct_answer}.")
    else:
        if user_input.lower() == "n":
            print("Correct!")
        else:
            print("Incorrect. The correct answer was 'no'.")

def start_quiz():
    while True:
        number = generate_number()
        print(f"Number: {number}")
        
        user_input = input("Enter the factor if it's a multiple of 12, or 'no' if it isn't: ")
        
        check_answer(number, user_input)
        
        continue_quiz = input("Do you want to try another number? (enter for yes): ")
        if continue_quiz.lower() != "":
            print("Thanks for practicing!")
            break

start_quiz()
