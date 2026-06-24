import os
import sys

import pytest

# Allow importing logic_utils from the project root when tests run from anywhere.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_utils import check_guess


# --- Starter tests, updated to the (outcome, message) contract ---------------
# check_guess returns a (outcome, message) tuple, so we unpack the outcome.

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Regression tests for the high/low hint bug ------------------------------
# FIX: Wrote this suite with the AI assistant to lock in the high/low bug fix,
# including the string-secret cases that originally flipped the hints.
class TestCheckGuessHighLowBug:
    """Regression tests for the high/low hint bug.

    The original check_guess fell into a string-comparison branch whenever the
    secret was passed as a str (app.py stringifies it on even attempts). That
    branch returned swapped hints -- e.g. a guess that was Too High told the
    player to "Go HIGHER!". These tests pin down the correct behavior.
    """

    def test_too_high_says_go_lower(self):
        outcome, message = check_guess(60, 50)
        assert outcome == "Too High"
        assert "LOWER" in message
        assert "HIGHER" not in message

    def test_too_low_says_go_higher(self):
        outcome, message = check_guess(40, 50)
        assert outcome == "Too Low"
        assert "HIGHER" in message
        assert "LOWER" not in message

    def test_exact_guess_wins(self):
        outcome, _ = check_guess(50, 50)
        assert outcome == "Win"

    # The core of the bug: a string secret must not flip the high/low logic.
    def test_string_secret_too_high_still_says_lower(self):
        outcome, message = check_guess(60, "50")
        assert outcome == "Too High"
        assert "LOWER" in message
        assert "HIGHER" not in message

    def test_string_secret_too_low_still_says_higher(self):
        outcome, message = check_guess(40, "50")
        assert outcome == "Too Low"
        assert "HIGHER" in message
        assert "LOWER" not in message

    def test_string_secret_exact_match_wins(self):
        outcome, _ = check_guess(50, "50")
        assert outcome == "Win"

    @pytest.mark.parametrize(
        "guess, secret, expected",
        [
            (99, 50, "Too High"),
            (1, 50, "Too Low"),
            (99, "50", "Too High"),  # string secret, would have flipped before the fix
            (1, "50", "Too Low"),
        ],
    )
    def test_high_low_outcomes(self, guess, secret, expected):
        outcome, _ = check_guess(guess, secret)
        assert outcome == expected
