import random


print("Welcome to random number guessing game!")

scores = {}

user = input("What is your username? ")

while True:
    min_range_input = input("Please enter the minimum number: ")
    max_range_input = input("Please enter the maximum number: ")

    if not min_range_input.isdigit() or not max_range_input.isdigit():
        print("Please enter a number only")
        continue

    min_range = int(min_range_input)
    max_range = int(max_range_input)

    if min_range > max_range:
        print("Minimum number must be smaller than maximum number")
    elif min_range == max_range:
        print("Minimum number cannot be same as maximum number")
        continue

    secret_number = random.randint(min_range, max_range)
    attempts = 0

    print(f"\nPlease start guessing a number from {min_range} to {max_range}")

    while True:
        guess = input("Type in your guess: ")

        if not guess.isdigit():
            print("Only numbers are allowed")
            continue

        guess = int(guess)
        attempts += 1

        if guess < secret_number:
            print("Your guess is too low")
        elif guess > secret_number:
            print("Your guess is too high")
        else:
            print(f"Great Job!! You got it right with {attempts} attempts")

            if user not in scores:
                scores[user] = []
            scores[user].append(attempts)
            break

    play_again = input("Would you like to play again? (y/n): ").lower()
    if play_again != "y":
        print("\nScore Board:")

        if scores:
            for user,attempts_list in scores.items():
                attempts_str = ','.join(str(a) for a in attempts_list)
                print(f"- {user}: {attempts_str}")
        else:
            print("There are no score record or history")

        print("Thank you for playing!")
        break