import tkinter as tk
import random

# --- Word Themes, Difficulty Levels, and Easy-mode Hints ---
WORD_THEMES = {
    "Animals": {
        "easy": [
            ("cat", "A small pet that says meow "),
            ("dog", "A loyal pet that barks "),
            ("fish", "Lives underwater "),
            ("bird", "It can fly and chirp "),
            ("cow", "Gives us milk "),
            ("pig", "Oinks on the farm "),
            ("ant", "Tiny insect, lives in colonies "),
            ("frog", "Jumps and croaks "),
            ("bee", "Makes honey "),
            ("rat", "Small rodent often found in cities ")
        ],
        "medium": [
            "rabbit", "zebra", "turtle", "monkey", "parrot",
            "sheep", "horse", "snake", "fox", "goat"
        ],
        "hard": [
            "chameleon", "crocodile", "kangaroo", "hippopotamus", "armadillo",
            "rhinoceros", "porcupine", "alligator", "chimpanzee", "flamingo"
        ]
    },
    "Fruits": {
        "easy": [
            ("apple", "Keeps the doctor away "),
            ("pear", "Green fruit shaped like a teardrop "),
            ("grape", "Small and grows in bunches "),
            ("mango", "Sweet tropical fruit "),
            ("kiwi", "Brown fuzzy fruit with green inside "),
            ("plum", "Purple and juicy fruit "),
            ("melon", "Big and sweet"),
            ("lime", "Green citrus fruit"),
            ("peach", "Soft fruit with fuzzy skin"),
        ],
        "medium": [
            "orange", "banana", "papaya", "cherry", "guava",
            "lemon", "tangerine", "blueberry", "apricot", "nectarine"
        ],
        "hard": [
            "pomegranate", "blackberry", "watermelon", "pineapple", "raspberry",
            "cranberry", "cantaloupe", "mulberry", "passionfruit", "dragonfruit"
        ]
    },
    "Countries": {
        "easy": [
            ("japan", "Land of the rising sun"),
            ("china", "The most populated country"),
            ("spain", "Known for flamenco"),
            ("italy", "Home of pizza and pasta"),
            ("korea", "Famous for group singer/dancer"),
            ("india", "Land of spices and Bollywood"),
            ("egypt", "Home of the pyramids"),
            ("greece", "Known for ancient mythology"),
            ("mexico", "Famous for tacos and sombreros"),
            ("turkey", "Famous for Istanbul and kebabs")
        ],
        "medium": [
            "canada", "france", "brazil", "germany", "vietnam",
            "indonesia", "thailand", "malaysia", "norway", "sweden"
        ],
        "hard": [
            "australia", "philippines", "argentina", "switzerland", "portugal",
            "netherlands", "denmark", "austria", "hungary", "finland"
        ]
    }
}


class WordGuessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Mystery Word Guess Game")
        self.root.geometry("500x500")
        self.root.config(bg="#F4F4F4")

        self.username = ""
        self.theme = None
        self.difficulty = None
        self.secret_word = ""
        self.hint = ""
        self.guessed_letters = []
        self.tries = 6
        self.score = 0

        self.create_start_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_back_button(self, command):
        """Creates a back button at top-left corner."""
        tk.Button(self.root, text="<", font=("Arial", 12, "bold"),
                  bg="#FFC107", fg="black", command=command).place(x=10, y=10)

    # --- Start Screen ---
    def create_start_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="🎯 Mystery Word Guess Game", font=("Arial", 18, "bold"), bg="#F4F4F4").pack(pady=40)
        tk.Button(self.root, text="Start Game ▶️", font=("Arial", 14), bg="#4CAF50", fg="white",
                  command=self.check_username_or_ask).pack(pady=10)
        tk.Button(self.root, text="Exit ❌", font=("Arial", 14), bg="#E53935", fg="white",
                  command=self.root.destroy).pack(pady=10)

    def check_username_or_ask(self):
        """If username exists, skip to theme selection; else ask for username"""
        if self.username:
            self.choose_theme()
        else:
            self.ask_username()

    # --- Username Input Screen ---
    def ask_username(self):
        self.clear_screen()
        self.create_back_button(self.create_start_screen)
        tk.Label(self.root, text="Enter your username (5-10 characters):", font=("Arial", 14), bg="#F4F4F4").pack(pady=40)
        self.username_entry = tk.Entry(self.root, font=("Arial", 14), width=15, justify="center")
        self.username_entry.pack(pady=10)
        self.username_message = tk.Label(self.root, text="", font=("Arial", 12), fg="red", bg="#F4F4F4")
        self.username_message.pack(pady=5)
        self.char_counter = tk.Label(self.root, text="0 / 10", font=("Arial", 12), bg="#F4F4F4")
        self.char_counter.pack(pady=5)
        self.username_entry.bind("<KeyRelease>", self.update_char_counter)
        tk.Button(self.root, text="Submit ✅", font=("Arial", 14), bg="#2196F3", fg="white",
                  command=self.validate_username).pack(pady=20)

    def update_char_counter(self, event=None):
        current_length = len(self.username_entry.get())
        self.char_counter.config(text=f"{current_length} / 10")

    def validate_username(self):
        username = self.username_entry.get().strip()
        if len(username) < 5 or len(username) > 10:
            self.username_message.config(text="❌ Username must be 5 to 10 characters!")
        else:
            self.username = username
            self.choose_theme()

    # --- Theme Selection ---
    def choose_theme(self):
        self.clear_screen()
        # Back button skips username input if username exists
        self.create_back_button(self.ask_username if not self.username else self.create_start_screen)

        # Centering buttons in middle part
        middle_frame = tk.Frame(self.root, bg="#F4F4F4")
        middle_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(middle_frame, text=f"Hello, {self.username}! 🌍 Choose a Theme", font=("Arial", 16, "bold"), bg="#F4F4F4").pack(pady=20)
        for theme in WORD_THEMES.keys():
            tk.Button(middle_frame, text=theme, font=("Arial", 14), width=15,
                      command=lambda t=theme: self.choose_difficulty(t)).pack(pady=5)

    # --- Difficulty Selection ---
    def choose_difficulty(self, theme):
        self.theme = theme
        self.clear_screen()
        self.create_back_button(self.choose_theme)

        # Centering difficulty buttons
        middle_frame = tk.Frame(self.root, bg="#F4F4F4")
        middle_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(middle_frame, text=f"{self.username}, choose difficulty ({theme}):", font=("Arial", 16, "bold"), bg="#F4F4F4").pack(pady=20)
        tk.Button(middle_frame, text="Easy 🟢", font=("Arial", 14), width=15,
                  command=lambda: self.start_game("easy")).pack(pady=5)
        tk.Button(middle_frame, text="Medium 🟡", font=("Arial", 14), width=15,
                  command=lambda: self.start_game("medium")).pack(pady=5)
        tk.Button(middle_frame, text="Hard 🔴", font=("Arial", 14), width=15,
                  command=lambda: self.start_game("hard")).pack(pady=5)

    # --- Game Logic ---
    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.guessed_letters = []
        self.score = 0

        # Set tries based on difficulty
        if difficulty == "easy":
            self.tries = 15
            word_data = random.choice(WORD_THEMES[self.theme]["easy"])
            self.secret_word, self.hint = word_data
        elif difficulty == "medium":
            self.tries = 10
            self.secret_word = random.choice(WORD_THEMES[self.theme]["medium"])
            self.hint = ""
        else:  # hard
            self.tries = 5
            self.secret_word = random.choice(WORD_THEMES[self.theme]["hard"])
            self.hint = ""

        self.secret_word = self.secret_word.lower()
        self.clear_screen()
        self.display_game_screen()

    def display_game_screen(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Player: {self.username}", font=("Arial", 12, "bold"), bg="#F4F4F4").pack(pady=5)
        tk.Label(self.root, text=f"🧩 Theme: {self.theme} | Difficulty: {self.difficulty.title()}",
                 font=("Arial", 12, "bold"), bg="#F4F4F4").pack(pady=10)

        display_word = " ".join([letter if letter in self.guessed_letters else "_" for letter in self.secret_word])
        self.word_label = tk.Label(self.root, text=display_word, font=("Courier", 22, "bold"), bg="#F4F4F4")
        self.word_label.pack(pady=20)

        self.tries_label = tk.Label(self.root, text=f"❤️ Tries Left: {self.tries}", font=("Arial", 14), bg="#F4F4F4")
        self.tries_label.pack(pady=5)

        entry_frame = tk.Frame(self.root, bg="#F4F4F4")
        entry_frame.pack(pady=10)
        tk.Label(entry_frame, text="Enter a letter:", font=("Arial", 12), bg="#F4F4F4").pack(side=tk.LEFT, padx=5)
        self.guess_entry = tk.Entry(entry_frame, font=("Arial", 14), width=5, justify="center")
        self.guess_entry.pack(side=tk.LEFT)
        tk.Button(entry_frame, text="Submit", font=("Arial", 12), bg="#2196F3", fg="white",
                  command=self.check_guess).pack(side=tk.LEFT, padx=5)

        if self.difficulty == "easy":
            self.hint_label = tk.Label(self.root, text=f"💡 Hint: {self.hint}",
                                       font=("Arial", 12, "italic"), bg="#F4F4F4", fg="#555")
            self.hint_label.pack(pady=20)

        self.end_message_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"), bg="#F4F4F4", fg="#222")
        self.end_message_label.pack(pady=10)

        self.play_again_frame = tk.Frame(self.root, bg="#F4F4F4")
        self.play_again_frame.pack(pady=10)

    def check_guess(self):
        guess = self.guess_entry.get().lower().strip()
        self.guess_entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            self.end_message_label.config(text="❌ Please enter a single letter!")
            return

        if guess in self.guessed_letters:
            self.end_message_label.config(text="⚠️ You already guessed that letter!")
            return

        self.guessed_letters.append(guess)

        if guess in self.secret_word:
            self.score += 10
            self.end_message_label.config(text=f"✅ '{guess}' is correct!")
        else:
            self.tries -= 1
            self.score -= 5
            self.end_message_label.config(text=f"❌ '{guess}' is wrong!")

        self.update_display()

    def update_display(self):
        display_word = " ".join([letter if letter in self.guessed_letters else "_" for letter in self.secret_word])
        self.word_label.config(text=display_word)
        self.tries_label.config(text=f"❤️ Tries Left: {self.tries}")

        if "_" not in display_word:
            self.show_end_game_message(won=True)
        elif self.tries == 0:
            self.show_end_game_message(won=False)

    def show_end_game_message(self, won):
        self.guess_entry.config(state="disabled")
        for widget in self.play_again_frame.winfo_children():
            widget.destroy()

        if won:
            message = f"🎉 {self.username}, You Win! The word was: {self.secret_word.upper()}\n🏆 Score: {self.score}"
        else:
            message = f"💀 {self.username}, Game Over! The word was: {self.secret_word.upper()}\n🏆 Score: {max(self.score, 0)}"

        self.end_message_label.config(text=message)

        # Play Again button remembers username
        tk.Button(self.play_again_frame, text="Play Again", font=("Arial", 12),
                  bg="#4CAF50", fg="white", command=self.check_username_or_ask).pack(side=tk.LEFT, padx=10)
        tk.Button(self.play_again_frame, text="Exit", font=("Arial", 12),
                  bg="#E53935", fg="white", command=self.root.destroy).pack(side=tk.LEFT, padx=10)
        self.play_again_frame.update()


if __name__ == "__main__":
    root = tk.Tk()
    app = WordGuessGame(root)
    root.mainloop()
