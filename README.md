# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.** A Streamlit number-guessing game: the app
  picks a secret number in a range based on difficulty, and the player guesses,
  getting "higher/lower" hints and a score until they win or run out of attempts.
- [x] **Detail which bugs you found.** The high/low hints were backwards — the
  game told you to "Go HIGHER!" when your guess was already too high. The root
  cause was that `app.py` converts the secret to a *string* on every even
  attempt, which pushed `check_guess` into a string-comparison fallback branch
  that returned swapped hint messages.
- [x] **Explain what fixes you applied.** I refactored the four logic functions
  out of `app.py` into `logic_utils.py`, then fixed `check_guess` to coerce both
  the guess and the secret to `int` before comparing — so a string secret can no
  longer flip the high/low direction. I added a pytest suite (`tests/`) that
  covers both the normal and the string-secret cases as regression tests.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Start the app with `python -m streamlit run app.py` and open it in the browser.
2. In the sidebar, pick a difficulty (Easy/Normal/Hard). This sets the number
   range and the number of allowed attempts, shown in the sidebar captions.
3. Type a guess into "Enter your guess:" and click **Submit Guess 🚀**.
4. Read the hint: if your guess is too high it now correctly says **"📉 Go
   LOWER!"**, and if it's too low it says **"📈 Go HIGHER!"** — the hints point
   the right way on every attempt, including even-numbered ones.
5. Keep guessing toward the secret; the score updates after each attempt.
6. When you guess correctly the game shows balloons, your final score, and the
   secret number. Click **New Game 🔁** to reset and play again.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

Run with `python -m pytest tests/ -v` (full output is also saved in
[`test_results.txt`](test_results.txt)):

```
============================= test session starts =============================
collected 13 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  7%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 15%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 23%]
tests/test_game_logic.py::TestCheckGuessHighLowBug::test_too_high_says_go_lower PASSED [ 30%]
tests/test_game_logic.py::TestCheckGuessHighLowBug::test_too_low_says_go_higher PASSED [ 38%]
tests/test_game_logic.py::TestCheckGuessHighLowBug::test_exact_guess_wins PASSED [ 46%]
tests/test_game_logic.py::TestCheckGuessHighLowBug::test_string_secret_too_high_still_says_lower PASSED [ 53%]
tests/test_game_logic.py::TestCheckGuessHighLowBug::test_string_secret_too_low_still_says_higher PASSED [ 61%]
tests/test_game_logic.py::TestCheckGuessHighLowBug::test_string_secret_exact_match_wins PASSED [ 69%]
tests/test_game_logic.py::TestCheckGuessHighLowBug::test_high_low_outcomes[99-50-Too High0] PASSED [ 76%]
tests/test_game_logic.py::TestCheckGuessHighLowBug::test_high_low_outcomes[1-50-Too Low0] PASSED [ 84%]
tests/test_game_logic.py::TestCheckGuessHighLowBug::test_high_low_outcomes[99-50-Too High1] PASSED [ 92%]
tests/test_game_logic.py::TestCheckGuessHighLowBug::test_high_low_outcomes[1-50-Too Low1] PASSED [100%]

============================= 13 passed in 0.03s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
