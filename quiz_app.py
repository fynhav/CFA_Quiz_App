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

    # Load and shuffle questions once per session
    if "shuffled_df" not in st.session_state:
        df = load_questions(st.session_state.csv_file)
        # Shuffle the DataFrame randomly
        st.session_state.shuffled_df = df.sample(frac=1).reset_index(drop=True)

    shuffled_df = st.session_state.shuffled_df
    q_idx = st.session_state.current_question

    # If all questions are done, show final result
    if q_idx >= len(shuffled_df):
        st.write("Quiz finished! You've gone through all the questions.")
        display_score_bar()

        # Show a "Back to Main Menu" button
        if st.button("Back to Main Menu"):
            st.session_state.csv_file = None
            st.session_state.current_question = 0
            st.session_state.answered = False
            st.session_state.selected_answer = None
            st.session_state.score = 0
            st.rerun()
        return

    # ============ Display the Current Question ============

    # Extract question data
    question_text = shuffled_df.loc[q_idx, "question"]
    optionA = shuffled_df.loc[q_idx, "optionA"]
    optionB = shuffled_df.loc[q_idx, "optionB"]
    optionC = shuffled_df.loc[q_idx, "optionC"]
    optionD = shuffled_df.loc[q_idx, "optionD"]
    correct_ans = shuffled_df.loc[q_idx, "correctAnswer"]  # "A", "B", "C", or "D"
    explanation = shuffled_df.loc[q_idx, "explanation"]

    st.subheader(f"Question {q_idx + 1}")
    st.write(question_text)

    # Build labels for radio buttons (e.g. "A) Berlin")
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
        # If user changes their selection, allow new submission
        st.session_state.answered = False

    selected_label = st.radio(
        "Select your answer:",
        labels,
        index=0,
        key="radio_answer",
        on_change=on_choice_change
    )
    st.session_state.selected_answer = label_to_letter[selected_label]

    # ============ Buttons: Submit & Next Question ============

    col1, col2 = st.columns(2)
    submit_clicked = col1.button("Submit", disabled=st.session_state.answered)
    next_clicked = col2.button("Next Question")

    # If Submit clicked: check correctness, show explanation, update score
    if submit_clicked and not st.session_state.answered:
        st.session_state.answered = True
        # We consider this question answered, so increment current_question
        st.session_state.current_question += 1

        if st.session_state.selected_answer == correct_ans:
            st.success("Correct! ✅")
            st.session_state.score += 1
        else:
            # e.g. correct_ans is "C", so correct option is "C) {optionC}"
            correct_label = f"{correct_ans}) {shuffled_df.loc[q_idx, 'option' + correct_ans]}"
            st.error(f"Incorrect! The correct answer is {correct_label}")

        # Show explanation
        st.info(f"Explanation: {explanation}")

        # Display updated score bar
        display_score_bar()

    # If Next Question clicked, move on (rerun)
    if next_clicked and st.session_state.answered:
        # Reset selected answer
        st.session_state.selected_answer = None
        st.rerun()

    # ============ Back to Main Menu at Bottom of Page ============

    st.write("---")
    if st.button("Back to Main Menu"):
        st.session_state.csv_file = None
        st.session_state.current_question = 0
        st.session_state.answered = False
        st.session_state.selected_answer = None
        st.session_state.score = 0
        st.rerun()

def main():
    st.title("Quiz Menu")

    # If we haven't picked a chapter CSV yet, show menu
    if "csv_file" not in st.session_state or st.session_state.csv_file is None:
        st.write("**Please choose which chapter quiz you want to take:**")

        # -- Chapter 1
        if st.button("Chapter 1 - Introduction to ESG Investing"):
            st.session_state.csv_file = "chapter1.csv"  # update if needed
            st.session_state.current_question = 0
            st.session_state.answered = False
            st.session_state.selected_answer = None
            st.session_state.score = 0
            st.rerun()

        # -- Chapter 2
        if st.button("Chapter 2 - The ESG Market"):
            st.session_state.csv_file = "chapter2.csv"  # update if needed
            st.session_state.current_question = 0
            st.session_state.answered = False
            st.session_state.selected_answer = None
            st.session_state.score = 0
            st.rerun()

        # -- Chapter 3
        if st.button("Chapter 3 - Environmental Factors"):
            st.warning("Placeholder: No CSV attached yet.")
            # If you have a CSV for Chapter 3, replace the code below:
            # st.session_state.csv_file = "chapter3.csv"
            # st.session_state.current_question = 0
            # st.session_state.answered = False
            # st.session_state.selected_answer = None
            # st.session_state.score = 0
            # st.rerun()

        # -- Chapter 4
        if st.button("Chapter 4 - Social Factors"):
            st.warning("Placeholder: No CSV attached yet.")

        # -- Chapter 5
        if st.button("Chapter 5 - Governance Factors"):
            st.warning("Placeholder: No CSV attached yet.")

        # -- Chapter 6
        if st.button("Chapter 6 - Engagement and Stewardship"):
            st.warning("Placeholder: No CSV attached yet.")

        # -- Chapter 7
        if st.button("Chapter 7 - ESG Analysis, Valuation, and Integration"):
            st.warning("Placeholder: No CSV attached yet.")

        # -- Chapter 8
        if st.button("Chapter 8 - Integrated Portfolio Construction and Management"):
            st.warning("Placeholder: No CSV attached yet.")

        # -- Chapter 9
        if st.button("Chapter 9 - Investment Mandates, Portfolio Analytics, and Client Reporting"):
            st.warning("Placeholder: No CSV attached yet.")

        st.stop()  # Stop so we don't run quiz() below

    else:
        # We have chosen a CSV, run the quiz
        quiz()

if __name__ == "__main__":
    # Initialize session variables if not set
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