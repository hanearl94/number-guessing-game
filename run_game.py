from game.storage import ScoreManager
from game.core import GameEngine

# Create instances of ScoreManager and GameEngine
score_manager = ScoreManager()
engine = GameEngine(score_manager)

# Prompt user for username
user = input("What is your username? ")

# Get valid range input
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

# Initialize guesses list
guesses = []

print(f"Guess numbers between {min_range} and {max_range}. Type 'q' to quit.")

# Loop for guesses
while True:
    guess_input = input("Your guess: ")
    if guess_input.lower() == "q":
        break
    if not guess_input.isdigit():
        print("Please enter a number.")
        continue

    guess = int(guess_input)
    guesses.append(guess)

    # Play the game with current guesses
    result = engine.play_game(user, min_range, max_range, [guess])

    if "Correct!" in result["message"]:
        print(result["message"])
        if result["new_record"]:
            print("🎉 NEW RECORD!")
        break
    else:
        print(f"Attempt {len(guesses)} incorrect. Try again.")
