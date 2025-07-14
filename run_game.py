# run_game.py
import game

user = input("What is your username? ")

while True:
    min_range_input = input("Enter minimum number: ")
    max_range_input = input("Enter maximum number: ")

    if not min_range_input.isdigit() or not max_range_input.isdigit():
        print("Please enter numbers only.")
        continue

    min_range = int(min_range_input)
    max_range = int(max_range_input)

    if min_range >= max_range:
        print("Minimum must be less than maximum.")
        continue

    break

guesses = []

print(f"Guess numbers between {min_range} and {max_range}. Type 'q' to quit.")

while True:
    guess_input = input("Your guess: ")
    if guess_input.lower() == "q":
        break
    if not guess_input.isdigit():
        print("Please enter a number.")
        continue

    guess = int(guess_input)
    guesses.append(guess)

    result = game.play_game(user, min_range, max_range, [guess])

    if "Correct!" in result["message"]:
        print(result["message"])
        if result["new_record"]:
            print("🎉 NEW RECORD!")
        break
    else:
        print(f"Attempt {len(guesses)} incorrect. Try again.")
