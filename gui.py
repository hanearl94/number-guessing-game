# gui.py
import tkinter as tk
from tkinter import messagebox
import game

class GuessingGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")

        # Username input
        tk.Label(root, text="Username:").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        # Range inputs
        tk.Label(root, text="Minimum number:").pack()
        self.min_entry = tk.Entry(root)
        self.min_entry.pack()

        tk.Label(root, text="Maximum number:").pack()
        self.max_entry = tk.Entry(root)
        self.max_entry.pack()

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack()

        # Guess area
        self.guess_label = tk.Label(root, text="")
        self.guess_entry = tk.Entry(root)
        self.guess_button = tk.Button(root, text="Submit Guess", command=self.submit_guess)

        self.guesses = []

    def start_game(self):
        self.user = self.username_entry.get().strip()
        if not self.user:
            messagebox.showerror("Error", "Username required.")
            return

        try:
            self.min_value = int(self.min_entry.get())
            self.max_value = int(self.max_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
            return

        if self.min_value >= self.max_value:
            messagebox.showerror("Error", "Minimum must be less than maximum.")
            return

        self.guesses = []

        self.guess_label.config(text=f"Guess a number between {self.min_value} and {self.max_value}")
        self.guess_label.pack()
        self.guess_entry.pack()
        self.guess_button.pack()

    def submit_guess(self):
        guess_input = self.guess_entry.get()
        if not guess_input.isdigit():
            messagebox.showerror("Error", "Please enter a number.")
            return

        guess = int(guess_input)
        self.guesses.append(guess)

        result = game.play_game(self.user, self.min_value, self.max_value, [guess])

        if "Correct!" in result["message"]:
            messagebox.showinfo("Success", result["message"])
            if result["new_record"]:
                messagebox.showinfo("New Record", "🎉 NEW RECORD!")
            self.root.quit()
        else:
            self.guess_label.config(text=f"Attempt {len(self.guesses)} incorrect. Try again.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = GuessingGameApp(root)
    root.mainloop()
