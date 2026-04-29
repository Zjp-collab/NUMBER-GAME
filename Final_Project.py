"""
Number Guessing Game — Enhanced Edition
Features:
  - Single Player mode with hint system, guess history, timer, statistics
  - Computer Guessing mode (binary search AI)
  - Multiplayer mode (two players, alternating turns)
"""

import random
import time


# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────

DIFFICULTY_SETTINGS = {
    "easy":   {"range": (1, 50),  "max_attempts": 15, "label": "Easy   (1–50,  15 attempts)"},
    "medium": {"range": (1, 100), "max_attempts": 10, "label": "Medium (1–100, 10 attempts)"},
    "hard":   {"range": (1, 200), "max_attempts": 7,  "label": "Hard   (1–200,  7 attempts)"},
}

# Session-wide statistics (single player)
session_stats = {
    "rounds_played": 0,
    "rounds_won":    0,
    "total_attempts": 0,
    "best_attempts":  None,
    "best_time":      None,
    "total_time":     0.0,
}


# ─────────────────────────────────────────────
#  SHARED HELPERS
# ─────────────────────────────────────────────

def divider(char="─", width=42):
    print("  " + char * width)


def get_difficulty():
    """Prompt the player to select a difficulty level."""
    print("\n  Select difficulty:")
    for key, val in DIFFICULTY_SETTINGS.items():
        print(f"    [{key[0].upper()}] {val['label']}")

    choice = input("\n  Enter E / M / H: ").strip().lower()
    while choice not in ("e", "easy", "m", "medium", "h", "hard"):
        print("  Invalid choice. Please enter E, M, or H.")
        choice = input("\n  Enter E / M / H: ").strip().lower()

    if choice in ("e", "easy"):
        return "easy"
    elif choice in ("m", "medium"):
        return "medium"
    else:
        return "hard"


def get_valid_guess(low, high, prompt=None):
    """Prompt for a valid integer guess within [low, high]."""
    prompt = prompt or f"\n  Your guess ({low}–{high}): "
    raw = input(prompt).strip()

    while raw == "" or not raw.lstrip("-").isdigit() or int(raw) < low or int(raw) > high:
        if raw == "":
            print("  Please enter a number.")
        elif not raw.lstrip("-").isdigit():
            print(f"  ⚠  '{raw}' is not a valid number. Try again.")
        else:
            print(f"  ⚠  Out of range! Guess between {low} and {high}.")
        raw = input(prompt).strip()

    return int(raw)


def get_hint(secret, low, high, guess_history):
    """Return a hint string about the secret number."""
    hints = []

    if secret % 2 == 0:
        hints.append("The number is EVEN.")
    else:
        hints.append("The number is ODD.")

    if secret % 5 == 0:
        hints.append("The number is a multiple of 5.")

    if secret % 3 == 0:
        hints.append("The number is a multiple of 3.")

    midpoint = (low + high) // 2
    if secret <= midpoint:
        hints.append(f"The number is in the LOWER half ({low}–{midpoint}).")
    else:
        hints.append(f"The number is in the UPPER half ({midpoint + 1}–{high}).")

    # Filter out hints that repeat info already known from guess history
    if guess_history:
        highest_low  = max((g for g in guess_history if g < secret), default=low)
        lowest_high  = min((g for g in guess_history if g > secret), default=high)
        hints.append(f"The number is between {highest_low} and {lowest_high}.")

    return random.choice(hints)


def display_guess_history(guess_history, secret):
    """Print the player's guess history with directional indicators."""
    if not guess_history:
        print("  No guesses yet.")
        return
    print("  Guess history:")
    for i, g in enumerate(guess_history, 1):
        if g < secret:
            arrow = "↑ too low"
        elif g > secret:
            arrow = "↓ too high"
        else:
            arrow = "✓ correct"
        print(f"    {i:>2}. {g:>4}  —  {arrow}")


def format_time(seconds):
    """Format seconds into a human-readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    mins = int(seconds) // 60
    secs = seconds % 60
    return f"{mins}m {secs:.1f}s"


# ─────────────────────────────────────────────
#  MODE 1 — SINGLE PLAYER
# ─────────────────────────────────────────────

def play_single_player():
    """Single player round with hints, guess history, and timer."""
    difficulty = get_difficulty()
    settings   = DIFFICULTY_SETTINGS[difficulty]
    low, high  = settings["range"]
    max_tries  = settings["max_attempts"]

    secret        = random.randint(low, high)
    attempts      = 0
    correct       = False
    guess_history = []
    start_time    = time.time()

    print(f"\n  I've picked a number between {low} and {high}.")
    print(f"  You have {max_tries} attempt(s). Good luck!")
    print("  (Type 'hint' for a hint, 'history' to see past guesses)\n")
    divider()

    while attempts < max_tries and not correct:
        remaining = max_tries - attempts
        elapsed   = time.time() - start_time
        print(f"\n  Attempts remaining: {remaining}  |  Time: {format_time(elapsed)}")

        raw = input(f"\n  Your guess ({low}–{high}) or command: ").strip().lower()

        count_guess = False

        if raw == "hint":
            hint = get_hint(secret, low, high, guess_history)
            print(f"  💡  Hint: {hint}")
        elif raw == "history":
            display_guess_history(guess_history, secret)
        elif raw == "" or not raw.lstrip("-").isdigit():
            print(f"  ⚠  '{raw}' is not a valid number or command.")
        elif int(raw) < low or int(raw) > high:
            print(f"  ⚠  Out of range! Guess between {low} and {high}.")
        else:
            count_guess = True

        if count_guess:
            guess = int(raw)
            guess_history.append(guess)
            attempts += 1

            if guess < secret:
                print("  📉  Too Low!  Try higher.")
            elif guess > secret:
                print("  📈  Too High! Try lower.")
            else:
                correct = True

    elapsed = time.time() - start_time

    divider("=")
    if correct:
        print(f"  🎉  Correct! The number was {secret}.")
        print(f"  Solved in {attempts} attempt(s) and {format_time(elapsed)}.")
    else:
        print(f"  💀  Out of attempts! The number was {secret}.")
        print("  Better luck next time!")
    divider("=")

    display_guess_history(guess_history, secret)

    # Update session stats
    session_stats["rounds_played"] += 1
    session_stats["total_time"]    += elapsed
    if correct:
        session_stats["rounds_won"]      += 1
        session_stats["total_attempts"]  += attempts
        if session_stats["best_attempts"] is None or attempts < session_stats["best_attempts"]:
            session_stats["best_attempts"] = attempts
        if session_stats["best_time"] is None or elapsed < session_stats["best_time"]:
            session_stats["best_time"] = elapsed

    return correct


# ─────────────────────────────────────────────
#  MODE 2 — COMPUTER GUESSING (Binary Search)
# ─────────────────────────────────────────────

def play_computer_guessing():
    """
    The player thinks of a number; the computer guesses it
    using binary search — guaranteed to solve in at most
    ceil(log2(range)) attempts.
    """
    print("\n  Think of a number and I'll guess it!")
    difficulty = get_difficulty()
    settings   = DIFFICULTY_SETTINGS[difficulty]
    low, high  = settings["range"]

    print(f"\n  Think of a number between {low} and {high}.")
    print("  Don't tell me — I'll figure it out!\n")
    divider()

    lo          = low
    hi          = high
    attempts    = 0
    found       = False
    start_time  = time.time()

    while lo <= hi and not found:
        mid      = (lo + hi) // 2
        attempts += 1

        print(f"\n  Attempt {attempts}: Is your number {mid}?")
        print("  Enter:  H = too high  |  L = too low  |  C = correct")
        response = input("  Your response: ").strip().upper()

        while response not in ("H", "L", "C"):
            print("  Please enter H, L, or C.")
            response = input("  Your response: ").strip().upper()

        if response == "C":
            found = True
        elif response == "H":
            hi = mid - 1
        else:
            lo = mid + 1

    elapsed = time.time() - start_time
    divider("=")
    if found:
        print(f"  🤖  I guessed it! Your number was {mid}.")
        print(f"  Solved in {attempts} attempt(s) and {format_time(elapsed)}.")
        print("  Binary search always wins! 😎")
    else:
        print("  🤔  I couldn't find your number.")
        print("  Are you sure you answered all the prompts correctly?")
    divider("=")


# ─────────────────────────────────────────────
#  MODE 3 — MULTIPLAYER
# ─────────────────────────────────────────────

def get_player_name(player_num):
    """Prompt for a player name."""
    name = input(f"\n  Enter name for Player {player_num}: ").strip()
    while name == "":
        print("  Name cannot be empty.")
        name = input(f"\n  Enter name for Player {player_num}: ").strip()
    return name


def play_one_multiplayer_turn(player_name, secret, low, high, max_tries):
    """
    One player's turn in multiplayer mode.
    Returns the number of attempts taken, or None if they didn't guess it.
    """
    print(f"\n  {player_name}'s turn!")
    print(f"  Guess the number between {low} and {high}.")
    print(f"  You have {max_tries} attempt(s).\n")
    divider()

    attempts      = 0
    correct       = False
    guess_history = []

    while attempts < max_tries and not correct:
        remaining = max_tries - attempts
        print(f"\n  Attempts remaining: {remaining}")

        guess = get_valid_guess(low, high)
        guess_history.append(guess)
        attempts += 1

        if guess < secret:
            print("  📉  Too Low!  Try higher.")
        elif guess > secret:
            print("  📈  Too High! Try lower.")
        else:
            correct = True
            print(f"\n  🎉  {player_name} got it in {attempts} attempt(s)!")

    if not correct:
        print(f"\n  ❌  {player_name} didn't guess it.")

    display_guess_history(guess_history, secret)
    return attempts if correct else None


def play_multiplayer():
    """
    Two players take turns guessing the same secret number.
    Fewest attempts wins. Ties are possible.
    """
    print("\n  ── MULTIPLAYER MODE ──")
    print("  Both players guess the same secret number.")
    print("  Fewest attempts wins!\n")

    p1_name = get_player_name(1)
    p2_name = get_player_name(2)

    difficulty = get_difficulty()
    settings   = DIFFICULTY_SETTINGS[difficulty]
    low, high  = settings["range"]
    max_tries  = settings["max_attempts"]

    secret = random.randint(low, high)

    print(f"\n  Secret number chosen between {low} and {high}. Let's go!")

    # Player 1's turn
    input(f"\n  Press Enter when {p1_name} is ready (hide the screen from {p2_name})...")
    p1_attempts = play_one_multiplayer_turn(p1_name, secret, low, high, max_tries)

    # Clear screen between turns
    print("\n" * 5)
    input(f"  Press Enter when {p2_name} is ready (hide the screen from {p1_name})...")
    p2_attempts = play_one_multiplayer_turn(p2_name, secret, low, high, max_tries)

    # Results
    divider("=")
    print(f"\n  ── RESULTS ──")
    print(f"  Secret number: {secret}")
    print(f"  {p1_name}: {'❌ Did not guess it' if p1_attempts is None else f'✅ {p1_attempts} attempt(s)'}")
    print(f"  {p2_name}: {'❌ Did not guess it' if p2_attempts is None else f'✅ {p2_attempts} attempt(s)'}")
    print()

    if p1_attempts is None and p2_attempts is None:
        print("  Neither player guessed it. It's a draw!")
    elif p1_attempts is None:
        print(f"  🏆  {p2_name} wins!")
    elif p2_attempts is None:
        print(f"  🏆  {p1_name} wins!")
    elif p1_attempts < p2_attempts:
        print(f"  🏆  {p1_name} wins with fewer attempts!")
    elif p2_attempts < p1_attempts:
        print(f"  🏆  {p2_name} wins with fewer attempts!")
    else:
        print(f"  🤝  It's a tie! Both guessed it in {p1_attempts} attempt(s).")

    divider("=")


# ─────────────────────────────────────────────
#  STATISTICS DISPLAY
# ─────────────────────────────────────────────

def display_statistics():
    """Display session statistics for single player mode."""
    s = session_stats
    divider("═")
    print("  📊  SESSION STATISTICS")
    divider("═")
    print(f"  Rounds played  : {s['rounds_played']}")
    print(f"  Rounds won     : {s['rounds_won']}")

    if s["rounds_played"] > 0:
        win_rate = (s["rounds_won"] / s["rounds_played"]) * 100
        print(f"  Win rate       : {win_rate:.1f}%")

    if s["rounds_won"] > 0:
        avg_attempts = s["total_attempts"] / s["rounds_won"]
        print(f"  Avg attempts   : {avg_attempts:.1f}  (winning rounds)")
        print(f"  Best round     : {s['best_attempts']} attempt(s)")
        print(f"  Fastest win    : {format_time(s['best_time'])}")

    print(f"  Total time     : {format_time(s['total_time'])}")
    divider("═")


# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────

def get_mode():
    """Display the main menu and return the selected mode."""
    print("\n  Select a game mode:")
    print("    [1] Single Player")
    print("    [2] Computer Guesses Your Number")
    print("    [3] Multiplayer (2 Players)")
    print("    [S] View Statistics")
    print("    [Q] Quit")

    choice = input("\n  Enter choice: ").strip().lower()
    while choice not in ("1", "2", "3", "s", "q"):
        print("  Invalid choice. Enter 1, 2, 3, S, or Q.")
        choice = input("\n  Enter choice: ").strip().lower()
    return choice


def main():
    print("\n" + "═" * 44)
    print("     🎯  NUMBER GUESSING GAME  🎯")
    print("         ── Enhanced Edition ──")
    print("═" * 44)

    running = True
    while running:
        mode = get_mode()

        if mode == "1":
            play_single_player()
        elif mode == "2":
            play_computer_guessing()
        elif mode == "3":
            play_multiplayer()
        elif mode == "s":
            display_statistics()
        else:
            running = False

    print("\n  Thanks for playing! Goodbye. 👋\n")


if __name__ == "__main__":
    main()