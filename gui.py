import tkinter as tk
from tkinter import messagebox
from game.storage import ScoreManager
from game.core import GameEngine
import random
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GuessingGameApp:
    """
    Tkinter GUI Application for Number Guessing Game
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")

        # Initialize ScoreManager and GameEngine
        self.score_manager = ScoreManager()
        self.engine = GameEngine(self.score_manager)

        self.main_menu()

    def main_menu(self):
        """
        Display the main menu with options
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Welcome to Number Guessing Game!", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Start Game", width=20, command=self.username_screen).pack(pady=5)
        tk.Button(self.root, text="View Leaderboard", width=20, command=self.show_leaderboard).pack(pady=5)
        tk.Button(self.root, text="Exit", width=20, command=self.root.quit).pack(pady=5)

    def username_screen(self):
        """
        Screen to enter username
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enter Username:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        self.username_entry.focus()
        self.username_entry.bind("<Return>", lambda event: self.range_screen())

        tk.Button(self.root, text="Next", command=self.range_screen).pack(pady=5)
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack()

    def range_screen(self):
        """
        Screen to enter min and max range
        """
        self.user = self.username_entry.get().strip()
        if not self.user:
            messagebox.showerror("Error", "Username required.")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Hi {self.user}! Enter range:").pack(pady=5)

        tk.Label(self.root, text="Minimum number:").pack()
        self.min_entry = tk.Entry(self.root)
        self.min_entry.pack()
        self.min_entry.focus()

        tk.Label(self.root, text="Maximum number:").pack()
        self.max_entry = tk.Entry(self.root)
        self.max_entry.pack()

        self.min_entry.bind("<Return>", lambda event: self.max_entry.focus())
        self.max_entry.bind("<Return>", lambda event: self.start_game())

        tk.Button(self.root, text="Start Game", command=self.start_game).pack(pady=5)
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack()

    def start_game(self):
        """
        Start the guessing game
        """
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
        self.secret_number = random.randint(self.min_value, self.max_value)

        for widget in self.root.winfo_children():
            widget.destroy()

        self.guess_label = tk.Label(self.root, text=f"Guess between {self.min_value} and {self.max_value}")
        self.guess_label.pack()

        self.guess_entry = tk.Entry(self.root)
        self.guess_entry.pack()
        self.guess_entry.focus()
        self.guess_entry.bind("<Return>", lambda event: self.submit_guess())

        tk.Button(self.root, text="Submit Guess", command=self.submit_guess).pack()
        tk.Button(self.root, text="Quit Game", command=self.main_menu).pack()

    def submit_guess(self):
        """
        Handle guess submission
        """
        guess_input = self.guess_entry.get()
        if not guess_input.isdigit():
            messagebox.showerror("Error", "Please enter a number.")
            self.guess_entry.delete(0, tk.END)
            return

        guess = int(guess_input)
        self.guesses.append(guess)

        if guess < self.secret_number:
            self.guess_label.config(text=f"Attempt {len(self.guesses)}: {guess} is too low.")
            self.guess_entry.delete(0, tk.END)
        elif guess > self.secret_number:
            self.guess_label.config(text=f"Attempt {len(self.guesses)}: {guess} is too high.")
            self.guess_entry.delete(0, tk.END)
        else:
            # Save result
            today = datetime.now().strftime("%Y-%m-%d")
            scores = self.score_manager.load_scores()
            if self.user not in scores:
                scores[self.user] = []
            scores[self.user].append({"date": today, "attempts": len(self.guesses)})
            self.score_manager.save_scores(scores)

            new_record = False
            if len(scores[self.user]) == 1:
                new_record = True
            else:
                best_attempts = min(r['attempts'] for r in scores[self.user][:-1])
                if len(self.guesses) < best_attempts:
                    new_record = True

            msg = f"Correct! You guessed the number {self.secret_number} in {len(self.guesses)} attempts."
            messagebox.showinfo("Success", msg)
            if new_record:
                messagebox.showinfo("New Record", "🎉 NEW RECORD!")

            self.main_menu()

    def show_leaderboard(self):
        """
        Display leaderboard and bar chart
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Leaderboard", font=("Arial", 16)).pack(pady=10)

        scores = self.score_manager.load_scores()
        if not scores:
            tk.Label(self.root, text="No records yet.").pack()
        else:
            user_averages = []
            for user_name, attempts_list in scores.items():
                total_attempts = sum(r['attempts'] for r in attempts_list)
                avg = total_attempts / len(attempts_list)
                user_averages.append((user_name, avg))

            sorted_users = sorted(user_averages, key=lambda x: x[1])

            for rank, (user_name, avg) in enumerate(sorted_users, start=1):
                tk.Label(self.root, text=f"{rank}. {user_name}: Avg Attempts {avg:.2f}").pack()

            users = [u for u, _ in sorted_users]
            averages = [a for _, a in sorted_users]

            fig, ax = plt.subplots(figsize=(5,3))

            # Prepare bar chart data
            users = [u for u, _ in sorted_users]
            averages = [a for _, a in sorted_users]

            # Generate random pastel colors for each user
            colors = []
            for _ in users:
                r = random.uniform(0.4, 0.9)
                g = random.uniform(0.4, 0.9)
                b = random.uniform(0.4, 0.9)
                colors.append((r, g, b))

            fig, ax = plt.subplots(figsize=(5, 3))
            ax.bar(users, averages, color=colors)
            ax.set_title("Average Attempts per User")
            ax.set_ylabel("Average Attempts")
            ax.set_ylim(0, max(averages) + 1)

            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

            ax.set_title("Average Attempts per User")
            ax.set_ylabel("Average Attempts")
            ax.set_ylim(0, max(averages)+1)

            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=10)

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = GuessingGameApp(root)
    root.mainloop()
