import json
import os

class ScoreManager:
    """
    This class handles loading and saving scores to JSON.
    """

    def __init__(self, filename="score.json"):
        self.filename = filename

    def load_scores(self):
        """
        Load scores from the JSON file.
        Returns an empty dict if file doesn't exist or invalid.
        """
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    data = json.load(f)
                    # Validate data structure
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
                # If error, return empty scores
                return {}
        else:
            return {}

    def save_scores(self, scores):
        """
        Save the scores dictionary to JSON file.
        """
        with open(self.filename, "w") as f:
            json.dump(scores, f, indent=2)
