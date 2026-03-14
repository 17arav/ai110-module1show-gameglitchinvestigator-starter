def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
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

    return True, value, None

# FIX: Separated check_guess (outcome) and guess_message (hint text) to fix inverted hints. Refactored from app.py using Copilot Agent mode.
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
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
    """Return a user-facing hint message for an outcome."""
    if outcome == "Win":
        return "🎉 Correct!"
    if outcome == "Too High":
        return "📉 Go LOWER!"
    if outcome == "Too Low":
        return "📈 Go HIGHER!"
    return ""


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
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
