import random

print("Welcome to random number guessing game!")
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
            print("Wow great job!")
            print(f"You got it right with {attempts} attempts")
            break

    play_again = input("Would you like to play again? (y/n): ").lower()
    if play_again != "y":
        print("Thank you for playing!")
        break