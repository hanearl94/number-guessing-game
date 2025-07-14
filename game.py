# game.py

import random
import json
import os
from datetime import datetime

# JSON file to store the scores
score_file = 'score.json'

def load_scores():
    """
    Load scores from the JSON file.
    If the file does not exist or is invalid, return an empty dictionary.
    """
    if os.path.exists(score_file):
        try:
            with open(score_file, "r") as f:
                data = json.load(f)
                # Validate the data structure
                if isinstance(data, dict):
                    for user_name, records in data.items():
                        if not isinstance(records, list):
                            raise ValueError
                        for record in records:
                            if not isinstance(record, dict) or 'attempts' not in record or 'date' not in record:
                                raise ValueError
                    return data
                else:
                    raise ValueError
        except Exception:
            # If reading fails, reset scores
            return {}
    else:
        # File does not exist, start fresh
        return {}

def save_scores(scores):
    """
    Save the scores dictionary to the JSON file.
    """
    with open(score_file, "w") as f:
        json.dump(scores, f, indent=2)

def play_game(user, min_range, max_range, guesses):
    """
    Core logic of the number guessing game.

    Arguments:
        user (str): The username.
        min_range (int): Minimum number of the range.
        max_range (int): Maximum number of the range.
        guesses (list[int]): List of guessed numbers.

    Returns:
        dict: {
            "message": str - final message,
            "new_record": bool - True if this is the best attempt,
            "scoreboard": dict - the full scoreboard
        }
    """
    # Load existing scores
    scores = load_scores()

    # Generate the secret random number
    secret_number = random.randint(min_range, max_range)

    attempts = 0
    messages = []

    # Process each guess
    for guess in guesses:
        if not isinstance(guess, int):
            # Skip invalid inputs
            messages.append("Invalid input, skipping.")
            continue

        attempts += 1

        if guess < secret_number:
            messages.append(f"Attempt {attempts}: {guess} is too low.")
        elif guess > secret_number:
            messages.append(f"Attempt {attempts}: {guess} is too high.")
        else:
            # Correct guess
            today = datetime.now().strftime("%Y-%m-%d")

            # Initialize user record if not exists
            if user not in scores:
                scores[user] = []

            # Save the current attempt
            scores[user].append({"date": today, "attempts": attempts})
            save_scores(scores)

            # Determine if this is a new record
            new_record = False
            if len(scores[user]) == 1:
                new_record = True
            else:
                best_attempts = min(r['attempts'] for r in scores[user][:-1])
                if attempts < best_attempts:
                    new_record = True

            # Return success result
            return {
                "message": f"Correct! You guessed the number {secret_number} in {attempts} attempts.",
                "new_record": new_record,
                "scoreboard": scores
            }

    # If no correct guess was made
    return {
        "message": "You did not guess the number.",
        "new_record": False,
        "scoreboard": scores
    }
