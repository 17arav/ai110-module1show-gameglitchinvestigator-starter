import random
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    guess_message,
    read_high_score,
    write_high_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "last_processed" not in st.session_state:
    st.session_state.last_processed = ""

# Show guess history in the sidebar
# Show high score and guess history in the sidebar
st.sidebar.subheader("High Score")
current_high = read_high_score()
if current_high:
    st.sidebar.metric("High Score", current_high)
else:
    st.sidebar.info("No high score yet.")

st.sidebar.subheader("Guess History")
if not st.session_state.history:
    st.sidebar.info("No guesses yet.")
else:
    rows = []
    secret_val = st.session_state.secret
    for idx, g in enumerate(st.session_state.history, start=1):
        try:
            val = int(g)
            diff = abs(val - secret_val)
            # Hot/Cold logic
            if diff == 0:
                hotcold = "🎉"
                color = "#4CAF50"  # green
                hint = "Correct"
            elif diff <= 5:
                hotcold = "🔥"
                color = "#4CAF50"  # green
                hint = "Very Close"
            elif diff <= 20:
                hotcold = "😐"
                color = "#FFD700"  # yellow
                hint = "Getting Warmer"
            else:
                hotcold = "🧊"
                color = "#F44336"  # red
                hint = "Far Away"
            direction = "Lower" if val > secret_val else (
                "Higher" if val < secret_val else "Correct"
            )
            rows.append({
                "Attempt": idx,
                "Guess": val,
                "Diff": diff,
                "Direction": direction,
                "Hot/Cold": hotcold,
                "Hint": hint,
                "Color": color
            })
        except Exception:
            rows.append({
                "Attempt": idx,
                "Guess": str(g),
                "Diff": "",
                "Direction": "Invalid",
                "Hot/Cold": "❓",
                "Hint": "Invalid",
                "Color": "#F44336"
            })

    # Sidebar table (simple)
    st.sidebar.table([
        {k: v for k, v in row.items() if k in ["Attempt", "Guess", "Direction", "Hot/Cold"]}
        for row in rows
    ])

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

    # FIX: Reset all session state variables (status, score, history) using Copilot Agent mode
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.last_processed = ""
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

# Process guess only if button clicked OR new input entered (not same as last time)
should_process = submit or (
    raw_guess and raw_guess != st.session_state.last_processed
)

if should_process:
    if not raw_guess:
        st.error("Enter a guess.")
        st.stop()

    st.session_state.last_processed = raw_guess
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret

        outcome = check_guess(guess_int, secret)
        message = guess_message(outcome)

        if show_hint:
            # Enhanced hint with color and emoji
            if ok:
                diff = abs(guess_int - st.session_state.secret)
                if diff == 0:
                    color = "#4CAF50"
                    emoji = "🎉"
                    hint = "Correct!"
                elif diff <= 5:
                    color = "#4CAF50"
                    emoji = "🔥"
                    hint = "Very Close!"
                elif diff <= 20:
                    color = "#FFD700"
                    emoji = "😐"
                    hint = "Getting Warmer"
                else:
                    color = "#F44336"
                    emoji = "🧊"
                    hint = "Far Away"
                st.markdown(
                    f'<span style="color:{color};font-size:1.2em">{emoji} {hint}</span>',
                    unsafe_allow_html=True
                )
            else:
                st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            # Update high score if this win beats it
            prev_high = read_high_score()
            if st.session_state.score > prev_high:
                write_high_score(st.session_state.score)
                st.sidebar.metric("High Score", st.session_state.score)
                st.sidebar.success(f"New high score: {st.session_state.score}")

            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
            # Show summary table
            st.subheader("Game Summary")
            summary_rows = []
            secret_val = st.session_state.secret
            for idx, g in enumerate(st.session_state.history, start=1):
                try:
                    val = int(g)
                    diff = abs(val - secret_val)
                    if diff == 0:
                        hotcold = "🎉"
                        color = "#4CAF50"
                        hint = "Correct"
                    elif diff <= 5:
                        hotcold = "🔥"
                        color = "#4CAF50"
                        hint = "Very Close"
                    elif diff <= 20:
                        hotcold = "😐"
                        color = "#FFD700"
                        hint = "Getting Warmer"
                    else:
                        hotcold = "🧊"
                        color = "#F44336"
                        hint = "Far Away"
                    direction = "Lower" if val > secret_val else (
                        "Higher" if val < secret_val else "Correct"
                    )
                    summary_rows.append({
                        "Attempt": idx,
                        "Guess": val,
                        "Diff": diff,
                        "Direction": direction,
                        "Hot/Cold": hotcold,
                        "Hint": hint
                    })
                except Exception:
                    summary_rows.append({
                        "Attempt": idx,
                        "Guess": str(g),
                        "Diff": "",
                        "Direction": "Invalid",
                        "Hot/Cold": "❓",
                        "Hint": "Invalid"
                    })
            st.table(summary_rows)
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
                # Show summary table
                st.subheader("Game Summary")
                summary_rows = []
                secret_val = st.session_state.secret
                for idx, g in enumerate(st.session_state.history, start=1):
                    try:
                        val = int(g)
                        diff = abs(val - secret_val)
                        if diff == 0:
                            hotcold = "🎉"
                            color = "#4CAF50"
                            hint = "Correct"
                        elif diff <= 5:
                            hotcold = "🔥"
                            color = "#4CAF50"
                            hint = "Very Close"
                        elif diff <= 20:
                            hotcold = "😐"
                            color = "#FFD700"
                            hint = "Getting Warmer"
                        else:
                            hotcold = "🧊"
                            color = "#F44336"
                            hint = "Far Away"
                        direction = "Lower" if val > secret_val else (
                            "Higher" if val < secret_val else "Correct"
                        )
                        summary_rows.append({
                            "Attempt": idx,
                            "Guess": val,
                            "Diff": diff,
                            "Direction": direction,
                            "Hot/Cold": hotcold,
                            "Hint": hint
                        })
                    except Exception:
                        summary_rows.append({
                            "Attempt": idx,
                            "Guess": str(g),
                            "Diff": "",
                            "Direction": "Invalid",
                            "Hot/Cold": "❓",
                            "Hint": "Invalid"
                        })
                st.table(summary_rows)

    # st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
