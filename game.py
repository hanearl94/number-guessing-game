import random
import json
import os
from datetime import datetime

print("Welcome to random number guessing game!")

score_file = 'score.json'

if os.path.exists(score_file):
    try:
        with open(score_file, "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                for user_name, records in data.items():
                    if not isinstance(records, list):
                        raise ValueError
                    for record in records:
                        if not isinstance(record, dict) or 'attempts' not in record or 'date' not in record:
                            raise ValueError
                scores = data
            else:
                raise ValueError
    except Exception:
        print("Warning: score.json is invalid or from old format. Resetting scores.")
        scores = {}
else:
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
            new_record = False
            if user in scores and scores[user]:
                previous_best = min(record['attempts'] for record in scores[user])
                if attempts < previous_best:
                    new_record = True
            else:
                new_record = True

            print(f"Great Job!! You got it right with {attempts} attempts")
            if new_record:
                print("!!! NEW RECORD !!!")

            today = datetime.now().strftime("%Y-%m-%d")

            if user not in scores:
                scores[user] = []

            scores[user].append({"date": today, "attempts": attempts})

            with open(score_file, "w") as f:
                json.dump(scores, f, indent=2)

            break

    play_again = input("Would you like to play again? (y/n): ").lower()
    if play_again != "y":
        print("\nScore Board:")

        if scores:
            user_averages = []
            for user_name, attempts_list in scores.items():
                total_attempts = sum(record['attempts'] for record in attempts_list)
                avg_attempts = total_attempts / len(attempts_list)
                user_averages.append((user_name, avg_attempts))

            sorted_users = sorted(user_averages, key=lambda x: x[1])

            print("\nLeaderboard (Lowest Average Attempts):")
            for rank, (user_name, avg) in enumerate(sorted_users, start=1):
                print(f"{rank}. {user_name} - Average Attempts: {avg:.2f}")

            print("\nDetailed Records:")
            for user_name,attempts_list in scores.items():
                print(f"\n- {user_name}:")
                for record in attempts_list:
                    print(f"  Date: {record['date']} - Attempts: {record['attempts']}")
        else:
            print("There are no score records or history")

        print("Thank you for playing!")
        break