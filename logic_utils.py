def get_range_for_difficulty(difficulty: str):
    """
    Return the inclusive (low, high) range for a given difficulty level.

    Args:
        difficulty (str): The difficulty setting ('Easy', 'Normal', 'Hard').

    Returns:
        tuple: (low, high) integer bounds for the guessing range.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str, low: int = 1, high: int = 100):
    """
    Parse user input into an integer guess and validate its range.

    Args:
        raw (str): The raw input string from the user.
        low (int): Minimum allowed value (inclusive).
        high (int): Maximum allowed value (inclusive).

    Returns:
        tuple: (ok, guess_int, error_message)
            ok (bool): True if parsing and validation succeeded.
            guess_int (int or None): Parsed integer guess, or None if invalid.
            error_message (str or None): Error message if parsing failed, else None.
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Please enter a number between {low} and {high}."

    return True, value, None
# FIX: Separated check_guess (outcome) and guess_message (hint text) to fix inverted hints. Refactored from app.py using Copilot Agent mode.
def check_guess(guess, secret):
    """
    Compare a guess to the secret number and return the outcome.

    Args:
        guess (int or str): The player's guess.
        secret (int or str): The secret number to compare against.

    Returns:
        str: Outcome label ('Win', 'Too High', 'Too Low').
    """
    # Normalize to integers when possible to avoid lexicographic surprises
    try:
        g = int(guess)
    except Exception:
        g = guess

    try:
        s = int(secret)
    except Exception:
        s = secret

    if g == s:
        return "Win"

    # If both are numbers do numeric compare
    if isinstance(g, int) and isinstance(s, int):
        if g > s:
            return "Too High"
        return "Too Low"

    # Fallback to default comparisons (string/other types)
    try:
        if g > s:
            return "Too High"
        return "Too Low"
    except Exception:
        return "Too Low"


def guess_message(outcome: str):
    """
    Return a user-facing hint message for a guess outcome.

    Args:
        outcome (str): The outcome label ('Win', 'Too High', 'Too Low').

    Returns:
        str: Hint message for the player.
    """
    if outcome == "Win":
        return "🎉 Correct!"
    if outcome == "Too High":
        return "📉 Go LOWER!"
    if outcome == "Too Low":
        return "📈 Go HIGHER!"
    return ""


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update the player's score based on the guess outcome and attempt number.

    Args:
        current_score (int): The current score before this guess.
        outcome (str): The outcome label ('Win', 'Too High', 'Too Low').
        attempt_number (int): The current attempt number (1-based).

    Returns:
        int: The updated score after applying scoring rules.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


def read_high_score(file_path: str = "high_score.txt") -> int:
    """
    Read the high score from a file.

    Args:
        file_path (str): Path to the high score file.

    Returns:
        int: The high score, or 0 if file is missing or invalid.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            content = fh.read().strip()
            return int(content)
    except Exception:
        return 0


def write_high_score(score: int, file_path: str = "high_score.txt") -> None:
    """
    Write the high score to a file, overwriting any existing value.

    Args:
        score (int): The score to record as the new high score.
        file_path (str): Path to the high score file.

    Returns:
        None
    """
    try:
        with open(file_path, "w", encoding="utf-8") as fh:
            fh.write(str(int(score)))
    except Exception:
        # best-effort; ignore write errors
        pass
