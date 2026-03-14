from logic_utils import check_guess, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(30, 50)
    assert result == "Too Low"


def test_parse_guess_decimal():
    # Decimal input should be converted to int by truncation
    ok, value, err = parse_guess("12.7")
    assert ok is True
    assert value == 12
    assert err is None


def test_parse_guess_negative_rejected():
    # Negative numbers are outside the default range and should be rejected
    ok, value, err = parse_guess("-5")
    assert ok is False
    assert value is None
    assert "between" in err


def test_check_guess_extremely_large_values():
    # Very large integers should compare numerically, not overflow
    big1 = 10 ** 50
    big2 = 10 ** 49
    assert check_guess(big1, big2) == "Too High"
    assert check_guess(big2, big1) == "Too Low"
