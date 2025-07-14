import random
from datetime import datetime

class GameEngine:
    """
    This class contains the core game logic:
    - Random number generation
    - Checking guesses
    - Recording scores
    """
    def __init__(self, score_manager):
        self.score_manager = score_manager

    def play_game(self, user, min_range, max_range, guesses):
        """
        Play the guessing game with provided guesses.
        Returns a dictionary with result information.
        """
        scores = self.score_manager.load_scores()
        secret_number = random.randint(min_range, max_range)
        attempts = 0

        for guess in guesses:
            if not isinstance(guess, int):
                continue

            attempts += 1

            if guess == secret_number:
                # Save the correct guess result
                today = datetime.now().strftime("%Y-%m-%d")
                if user not in scores:
                    scores[user] = []
                scores[user].append({"date": today, "attempts": attempts})
                self.score_manager.save_scores(scores)

                # Check if it's a new record
                new_record = False
                if len(scores[user]) == 1:
                    new_record = True
                else:
                    best_attempts = min(r['attempts'] for r in scores[user][:-1])
                    if attempts < best_attempts:
                        new_record = True

                return {
                    "message": f"Correct! You guessed in {attempts} attempts.",
                    "new_record": new_record,
                    "scoreboard": scores
                }

        # If no correct guess
        return {
            "message": "No correct guess.",
            "new_record": False,
            "scoreboard": scores
        }
