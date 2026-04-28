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