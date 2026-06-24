# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

When I first ran the game I saw a number guesser game.


- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  The game would continue to say "Go Lower" even when guessing the lowest possible number. The game also keeps the "You already won. Start a new game to play again." even after you start a new game, preventing another guess to submit.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 20    | go lower          | go higher       | none                   |
| 20    | go higher         | go higher       | none                   |
| 13    | go lower          | go higher       | none                   |

---

## 2. How did you use AI as a teammate?

I worked with Claude (Claude Code, running in agent mode inside VS Code). I used
it to refactor the code and to help diagnose the backwards-hint bug, giving it
multi-step instructions like "move the logic functions into `logic_utils.py`,
fix the high/low bug, and update the import in `app.py`."

A correct suggestion: it identified that the real cause of the backwards hints
was `app.py` turning the secret into a string on even attempts, which sent
`check_guess` into a fallback branch with swapped messages. It fixed this by
coercing both values to `int` before comparing. I verified the fix by running
`pytest` (all tests passed) and by reading the diff to confirm the logic.

A misleading/incorrect moment: when reorganizing the tests, the AI ran
`git mv test tests`, which accidentally nested the folder into `tests/test/`
because a `tests/` directory already existed. I caught this in the file listing
and had it clean the structure back to a single `tests/test_game_logic.py`. It
was a good reminder to check the AI's multi-step actions instead of assuming
they worked.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed when an automated test that reproduced it
started passing, not just when the app "looked" right. I ran
`python -m pytest tests/ -v` and watched all 13 tests pass, including the cases
that pass the secret in as a string. One test in particular,
`test_string_secret_too_high_still_says_lower`, checks `check_guess(60, "50")`
and asserts the hint says "LOWER"; it confirmed that my fix addressed the *root
cause* (a string secret) rather than just the obvious case. AI helped design the
tests — it suggested the string-secret edge cases, which were exactly the inputs
that triggered the original bug and which I might not have thought to test on my
own.

---

## 4. What did you learn about Streamlit and state?

I'd explain it like this: every time you click a button or type something,
Streamlit throws away the page and runs your whole script again from the top.
That means normal variables get recreated each time, so they can't remember
anything between clicks. To keep values that should survive — like the secret
number, the score, and how many attempts you've used — you store them in
`st.session_state`, which Streamlit preserves across those reruns. That's why
the secret is set once with `if "secret" not in st.session_state` instead of
every run.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is writing a test that reproduces the bug as part of
fixing it, so I have proof the fix works and a guard against it coming back.
Pulling the game logic out of the UI into `logic_utils.py` also made that
possible, since pure functions are much easier to test than Streamlit code.

Next time I'd give the AI smaller, checkable steps and verify each one — the
`git mv` mistake happened because I let a multi-step action run without
checking the result first.

This project changed how I think about AI-generated code: it can look polished
and "production-ready" while still hiding a subtle logic bug like swapped hints,
so I now treat AI output as a first draft to test and review, not something to
trust on sight.
