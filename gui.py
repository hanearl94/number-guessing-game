# gui.py
import tkinter as tk
from tkinter import messagebox
import game
import random
from datetime import datetime

class GuessingGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")

        self.main_menu()

    def main_menu(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Welcome to Number Guessing Game!", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Start Game", width=20, command=self.username_screen).pack(pady=5)
        tk.Button(self.root, text="View Leaderboard", width=20, command=self.show_leaderboard).pack(pady=5)
        tk.Button(self.root, text="Exit", width=20, command=self.root.quit).pack(pady=5)

    def username_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enter Username:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        self.username_entry.focus() #enabling cursor

        # Enter key binding
        self.username_entry.bind("<Return>", lambda event: self.range_screen())

        tk.Button(self.root, text="Next", command=self.range_screen).pack(pady=5)
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack()

    def range_screen(self):
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
        self.min_entry.focus()  # enabling cursor

        tk.Label(self.root, text="Maximum number:").pack()
        self.max_entry = tk.Entry(self.root)
        self.max_entry.pack()

        # Enter on min_entry moves focus to max_entry
        self.min_entry.bind("<Return>", lambda event: self.max_entry.focus())

        # Enter on max_entry starts the game
        self.max_entry.bind("<Return>", lambda event: self.start_game())

        tk.Button(self.root, text="Start Game", command=self.start_game).pack(pady=5)
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack()

    def start_game(self):
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
        self.guess_entry.focus()  # enabling cursor

        # Enter key binding
        self.guess_entry.bind("<Return>", lambda event: self.submit_guess())

        self.submit_button = tk.Button(self.root, text="Submit Guess", command=self.submit_guess)
        self.submit_button.pack()

        tk.Button(self.root, text="Quit Game", command=self.main_menu).pack()

    def submit_guess(self):
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
            # Save score
            today = datetime.now().strftime("%Y-%m-%d")
            scores = game.load_scores()
            if self.user not in scores:
                scores[self.user] = []
            scores[self.user].append({"date": today, "attempts": len(self.guesses)})
            game.save_scores(scores)

            # New record check
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
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Leaderboard", font=("Arial", 16)).pack(pady=10)

        scores = game.load_scores()
        if not scores:
            tk.Label(self.root, text="No records yet.").pack()
        else:
            user_averages = []
            for user_name, attempts_list in scores.items():
                total_attempts = sum(r['attempts'] for r in attempts_list)
                avg = total_attempts / len(attempts_list)
                user_averages.append((user_name, avg))

            sorted_users = sorted(user_averages, key=lambda x: x[1])

            # Show text leaderboard
            for rank, (user_name, avg) in enumerate(sorted_users, start=1):
                tk.Label(self.root, text=f"{rank}. {user_name}: Avg Attempts {avg:.2f}").pack()

            # Prepare bar chart data
            users = [u for u, _ in sorted_users]
            averages = [a for _, a in sorted_users]

            fig, ax = plt.subplots(figsize=(5, 3))
            ax.bar(users, averages, color='skyblue')
            ax.set_title("Average Attempts per User")
            ax.set_ylabel("Average Attempts")
            ax.set_ylim(0, max(averages) + 1)

            # Embed matplotlib figure in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=10)


# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = GuessingGameApp(root)
    root.mainloop()
