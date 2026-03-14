# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

Bug 1: New Game button not working

Expected: Clicking "New Game" should reset the game and generate a new secret number.
Actual: Nothing happens when I click the "New Game" button. The game stays in the same state.

Bug 2: Press Enter to submit not working

Expected: Pressing Enter after typing a guess should submit it.
Actual: Pressing Enter does nothing. I have to click the "Submit Guess" button manually.

Bug 3: Developer Debug Info is visible

Expected: Debug info showing the secret number should be hidden from players.
Actual: Anyone can expand "Developer Debug Info" and see the actual answer, which ruins the game.

Bug 4: Hints give wrong direction

Expected: If the secret number is 22 and I guess 0, the hint should say "go higher."
Actual: The hint says "go lower," which is the opposite of what it should say.

Bug 5: Game accepts numbers outside the valid range

Expected: The game should only accept guesses between 1 and 100.
Actual: I can enter numbers above 100 or below 1 and the game accepts them.

Bug 6: Score logic is unclear/broken

Expected: The score should make sense — like starting high and decreasing with each wrong guess.
Actual: The score doesn't seem to follow any logical pattern. It's hard to understand how it's calculated.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  I used GitHub Copilot Chat and Agent mode in VS Code, and also used Claude (Anthropic) to help understand the bugs and guide me through the project step by step.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  Copilot correctly identified that the hint messages in check_guess were swapped — "Go HIGHER" was showing when the guess was too high, and "Go LOWER" when too low. It also found that the secret number was sometimes being converted to a string, causing wrong comparisons. I verified this by running the game after the fix and checking that the hints now matched my guesses correctly.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  When Copilot first tried to run the tests with pytest -q, it failed with a ModuleNotFoundError because it didn't set up the import path correctly. It had to create a conftest.py file to fix the issue. I verified this by seeing the test fail the first time and then pass after the fix was applied.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  I decided a bug was fixed by testing it two ways: first by running the game in the browser with streamlit run app.py and manually checking the behavior, and second by running pytest -q to make sure the automated tests passed.
  
- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  I ran pytest -q which included a test called test_guess_too_high — it checks that when the guess is 60 and the secret is 50, check_guess returns "Too High". All 3 tests passed, confirming that the hint logic was fixed.

- Did AI help you design or understand any tests? How?
  Yes, I asked Copilot to generate pytest tests targeting the hint bug I fixed. It created tests for "Too High", "Too Low", and "Win" cases in test_game_logic.py. I verified the tests by running them in the terminal and seeing all 3 pass.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  Every time you click a button or interact with something in a Streamlit app, the entire Python script runs again from top to bottom — that's called a "rerun." This means any regular variable you create gets reset every time. To keep data between reruns (like the secret number, score, or game status), you use st.session_state, which is like a special storage box that remembers values even when the script reruns. For example, without session state, our secret number would change every time we clicked "Submit Guess," making the game impossible to win.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - I want to keep using the approach of finding and documenting bugs first before trying to fix them. Playing the game, writing down what I expected vs what actually happened, and then using AI to understand the root cause made the whole debugging process much smoother and organized.

- What is one thing you would do differently next time you work with AI on a coding task?
  Next time I would review AI-generated code changes more carefully before accepting them. For example, when Copilot made changes using Agent mode, I should have looked at every red and green line in the diff more closely instead of just clicking Keep right away.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  This project showed me that AI-generated code can look correct but still have serious bugs like swapped hint messages or unnecessary type conversions. I learned that I always need to test and verify AI code myself rather than trusting it blindly.
