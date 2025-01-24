import streamlit as st
import pandas as pd

@st.cache_data
def load_questions(csv_file):
    """Load the questions from the specified CSV file."""
    df = pd.read_csv(csv_file)
    return df

def display_score_bar():
    """
    Renders a horizontal bar showing the fraction of correct answers
    among the questions answered so far (green = correct, red = incorrect).
    """
    answered_count = st.session_state.current_question
    correct_count = st.session_state.score

    # If no questions answered yet, skip the bar
    if answered_count == 0:
        return

    correct_percentage = (correct_count / answered_count) * 100
    score_bar_html = f"""
    <div style="background-color: #ddd; width: 100%; height: 20px; position: relative; margin-top: 10px;">
        <div style="background-color: green; width: {correct_percentage}%; height: 20px; float: left;"></div>
        <div style="background-color: red; width: {100 - correct_percentage}%; height: 20px; float: left;"></div>
    </div>
    <p style="margin-top: 5px;">
        Correct: {correct_count} / {answered_count} ({correct_percentage:.1f}%)
    </p>
    """
    st.markdown(score_bar_html, unsafe_allow_html=True)

def quiz():
    """
    Runs the quiz flow using the CSV file in st.session_state.csv_file.
    """
    # --- Load and shuffle questions once per session/quiz
    if "shuffled_df" not in st.session_state:
        df = load_questions(st.session_state.csv_file)
        st.session_state.shuffled_df = df.sample(frac=1).reset_index(drop=True)

    shuffled_df = st.session_state.shuffled_df
    q_idx = st.session_state.current_question

    # If all questions are done, show final result
    if q_idx >= len(shuffled_df):
        st.write("Quiz finished! You've gone through all the questions.")
        display_score_bar()
        return

    # Retrieve row data
    question_text = shuffled_df.loc[q_idx, "question"]
    optionA = shuffled_df.loc[q_idx, "optionA"]
    optionB = shuffled_df.loc[q_idx, "optionB"]
    optionC = shuffled_df.loc[q_idx, "optionC"]
    optionD = shuffled_df.loc[q_idx, "optionD"]
    correct_ans = shuffled_df.loc[q_idx, "correctAnswer"]
    explanation = shuffled_df.loc[q_idx, "explanation"]

    # Display question
    st.subheader(f"Question {q_idx + 1}")
    st.write(question_text)

    # Build the label strings (e.g., "A) Berlin")
    labelA = f"A) {optionA}"
    labelB = f"B) {optionB}"
    labelC = f"C) {optionC}"
    labelD = f"D) {optionD}"

    labels = [labelA, labelB, labelC, labelD]
    label_to_letter = {
        labelA: "A",
        labelB: "B",
        labelC: "C",
        labelD: "D",
    }

    def on_choice_change():
        st.session_state.answered = False

    selected_label = st.radio(
        "Select your answer:",
        labels,
        index=0,
        key="radio_answer",
        on_change=on_choice_change
    )

    st.session_state.selected_answer = label_to_letter[selected_label]

    # Place Submit and Next Question side by side
    col1, col2 = st.columns(2)

    submit_clicked = col1.button("Submit", disabled=st.session_state.answered)
    next_clicked = col2.button("Next Question")

    # If Submit was clicked, process the current question
    if submit_clicked:
        st.session_state.answered = True
        st.session_state.current_question += 1  # Mark that we've answered one more question

        # Check correctness
        if st.session_state.selected_answer == correct_ans:
            st.success("Correct! ✅")
            st.session_state.score += 1
        else:
            correct_label = f"{correct_ans}) {shuffled_df.loc[q_idx, 'option' + correct_ans]}"
            st.error(f"Incorrect! The correct answer is {correct_label}")

        # Show explanation
        st.info(f"Explanation: {explanation}")

        # Display the score bar
        display_score_bar()

    # If Next Question is clicked, move on to the next question
    if next_clicked:
        # Reset the selected answer
        st.session_state.selected_answer = None
        # Rerun the app so the next question is displayed
        st.rerun()

def main():
    st.title("Quiz Menu")

    # If we haven't picked a chapter yet, show the menu
    if "csv_file" not in st.session_state or st.session_state.csv_file is None:
        st.write("**Please choose which chapter quiz you want to take:**")

        # Create a row of buttons for each quiz
        col1, col2, col3 = st.columns(3)

        # Example: you can add as many chapters as you want
        if col1.button("Chapter 1"):
            st.session_state.csv_file = "chapter1.csv"
            # Initialize quiz states
            st.session_state.current_question = 0
            st.session_state.answered = False
            st.session_state.selected_answer = None
            st.session_state.score = 0
            st.rerun()

        if col2.button("Chapter 2"):
            st.session_state.csv_file = "chapter2.csv"
            # Initialize quiz states
            st.session_state.current_question = 0
            st.session_state.answered = False
            st.session_state.selected_answer = None
            st.session_state.score = 0
            st.rerun()

        # Add more chapters as needed:
        # if col3.button("Chapter 3"):
        #     st.session_state.csv_file = "chapter3.csv"
        #     ... reset states ...
        #     st.experimental_rerun()

        st.stop()  # Stop execution so we don't run the quiz function
    else:
        # We've chosen a CSV, so run the quiz
        quiz()

if __name__ == "__main__":
    # Initialize any needed session keys if not set
    if "csv_file" not in st.session_state:
        st.session_state.csv_file = None
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "selected_answer" not in st.session_state:
        st.session_state.selected_answer = None
    if "score" not in st.session_state:
        st.session_state.score = 0

    main()

# cd /path/to/your/folder
# streamlit run quiz_app.py