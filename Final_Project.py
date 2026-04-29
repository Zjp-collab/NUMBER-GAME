"""
Number Guessing Game
Single Player, Terminal-Based
"""

import random


DIFFICULTY_SETTINGS = {
    "easy":   {"range": (1, 50), "max_attempts": 15, "label": "Easy  (1-50,  15 attempts)"},
    "medium": {"range": (1, 100), "max_attempts": 10, "label": "Medium (1-100, 10 attempts)"},
    "hard":   {"range": (1, 200), "max_attempts": 7, "label": "Hard   (1-200,  7 attempts)"}
}


def get_difficulty():
    """Prompts the player to select a difficulty level."""
    print("\n Select difficulty level: ")
    for key, val in DIFFICULTY_SETTINGS.items():
        print(f"  [{key[0].upper()}] {val['label']}")

    while True:
        choice = input("\n Enter E, M, or H: ").strip().lower()
        if choice in ("e", "easy"):
            return "easy"
        elif choice in ("m", "medium"):
            return "medium"
        elif choice in ("h", "hard"):
            return "hard"
        else:
            print(" Invalid choice. Please enter E, M, or H.")

def get_valid_guess(low, high):
    """Prompt the player for a valid integer guess within the given range"""
    raw = input(f"\n  Your guess ({low}-{high}): ").strip()

    while raw == "" or not raw.lstrip("-").isdigit() or int(raw) < low or int(raw) > high:
        if raw == "":
            print("  Please enter a guess.")
        elif not raw.lstrip("-").isdigit():
            print("  Invalid input. Please enter a number.")
        else:
            print(f"  Out of range. Please enter a number between {low} and {high}.")
        raw = input(f"  Your guess ({low}-{high}): ").strip()

    return int(raw)

def play_round():
    """Run one complete game round. Returns True if the player won."""
    difficulty = get_difficulty()
    settings = DIFFICULTY_SETTINGS[difficulty]
    low, high = settings["range"]
    max_tries = settings["max_attempts"]

    secret = random.randint(low, high)
    attempts = 0
    correct = False

    print(f"\n I've picked a number between {low} and {high}.")
    print(f" You have {max_tries} attempt(s). Good luck!\n")
    print("  " + "-" * 38)

    while attempts < max_tries and not correct:
        remaining = max_tries - attempts
        print(f"\n  Attempts remaining: {remaining}")

        guess = get_valid_guess(low, high)
        attempts += 1

        if guess < secret:
            print("  Too low! Try higher.")
        elif guess > secret:
            print("  Too high! Try lower.")
        else:
            correct = True
            print(f"\n  Congratulations! You've guessed the number {secret}.")
            print(f" You guessed it in {attempts} attempt(s)!")
            print("  " + "-" * 38)

    if not correct:
        print("\n  " + "-" * 38)
        print(f"  Game Over! The number was {secret}.")
        print("  Better luck next time!")
        print("  " + "-" * 38)

        return correct
    
def main():
    print("\n" + "=" * 42)
    print(" Welcome to the Number Guessing Game! ")
    print("=" * 42)

    again = "y"
    while again in ("y", "yes"):
        play_round()
        again = input("\n Would you like to play again? (Y/N): ").strip().lower()
        while again not in ("y", "yes", "n", "no"):
            print(" Invalid input. Please enter Y or N.")
            again = input(" Would you like to play again? (Y/N): ").strip().lower()

    print("\n Thanks for playing! Goodbye!\n")

if __name__ == "__main__":
    main()  
                  