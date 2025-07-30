import streamlit as st
import time
import json
from config import Questioner, Evaluator

st.set_page_config(page_title="I'm Arya, your Interviewer", layout="centered")

# --- UI X-Factors & Personalization ---
st.markdown("""
<style>
    .st-emotion-cache-1y4p8pa {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# --- Session State Initialization ---
if "step" not in st.session_state:
    st.session_state.step = "intro"
if "answers" not in st.session_state:
    st.session_state.answers = []
if "questions" not in st.session_state:
    st.session_state.questions = {"easy": [], "medium": [], "hard": []}
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "level_index" not in st.session_state:
    st.session_state.level_index = 0
if "timer_start" not in st.session_state:
    st.session_state.timer_start = 0.0
# Key for storing the current answer in session state
if "current_answer" not in st.session_state:
    st.session_state.current_answer = ""


levels = ["easy", "medium", "hard"]
time_limits = {"easy": 30, "medium": 45, "hard": 60}

# -------------------- STEP: INTRO --------------------
if st.session_state.step == "intro":
    st.title("✨ Welcome to Interview Prep with Arya✨")
    st.markdown("---")
    name = st.text_input("First, what should I call you?")
    topic = st.text_input("And what topic are we focusing on today?")
    num = st.number_input("How many questions per difficulty level?", min_value=1, max_value=5, value=2)

    if st.button("Let's Begin!", use_container_width=True):
        if name and topic:
            st.session_state.name = name
            st.session_state.topic = topic
            st.session_state.num = num
            st.session_state.step = "generate"
            st.rerun()
        else:
            st.error("Please fill in your name and topic to continue.")

# -------------------- STEP: GENERATE --------------------
elif st.session_state.step == "generate":
    st.title(f"Preparing Your Quiz, {st.session_state.name}...")
    qmodel = Questioner(st.session_state.topic, st.session_state.num)
    for level in levels:
        with st.spinner(f"Curating {level} questions with ARYA..."):
            st.session_state.questions[level] = qmodel.generate(level)
    st.session_state.step = "quiz"
    st.session_state.timer_start = time.time()
    st.rerun()

# -------------------- STEP: QUIZ --------------------
elif st.session_state.step == "quiz":
    level = levels[st.session_state.level_index]
    questions = st.session_state.questions[level]
    total = len(questions)
    i = st.session_state.current_question
    limit = time_limits[level]

    if i >= total:
        st.session_state.current_question = 0
        st.session_state.level_index += 1
        st.session_state.step = "evaluate" if st.session_state.level_index >= len(levels) else "quiz"
        st.session_state.timer_start = time.time()
        st.rerun()
    else:
        st.markdown(f"### {level.capitalize()} Question {i+1} of {total}")
        st.info(questions[i])

        with st.form(key=f"quiz_form_{level}_{i}", clear_on_submit=True):
            user_answer = st.text_area("Your Answer", key="user_input_widget", value=st.session_state.current_answer)
            submitted = st.form_submit_button("Submit")

            # This line ensures the session state is updated with the latest text
            st.session_state.current_answer = user_answer

            if submitted:
                st.session_state.answers.append({"level": level, "question": questions[i], "answer": st.session_state.current_answer})
                st.session_state.current_question += 1
                st.session_state.timer_start = time.time()
                st.session_state.current_answer = ""
                st.rerun()

        elapsed = time.time() - st.session_state.timer_start
        remaining_time = limit - elapsed

        if remaining_time > 0:
            st.progress(remaining_time / limit)
            st.caption(f"Time remaining: {int(remaining_time)} seconds")
            time.sleep(1)
            st.rerun()
        else:
            st.warning("Time's up!")
            answer_on_timeout = st.session_state.current_answer or "No answer (Time's up!)"
            st.session_state.answers.append({"level": level, "question": questions[i], "answer": answer_on_timeout})
            st.session_state.current_question += 1
            st.session_state.timer_start = time.time()
            st.session_state.current_answer = ""
            st.rerun()

# -------------------- STEP: EVALUATE --------------------
elif st.session_state.step == "evaluate":
    st.title(f"Evaluation by Arya for {st.session_state.name}")
    with st.spinner("Arya is analyzing your answers..."):
        paper = {"name": st.session_state.name, "topic": st.session_state.topic, "qa": st.session_state.answers}
        evaluator = Evaluator(topic=st.session_state.topic, paper=paper)
        result = evaluator.evaluate()
        st.session_state.result = result

    score = result.get('score', 0)
    st.metric("Final Score", f"{score} / 100")
    
    if score >= 70:
        st.balloons()
        st.success("Congratulations! You passed!")
    else:
        st.warning("You did not pass this time. Keep practicing!")

    st.info(f"**ARYA's Suggestion:** {result.get('suggestion', 'No feedback available.')}")
    st.markdown("---")
    if st.button("Chat with ARYA about your results", use_container_width=True):
        st.session_state.step = "chatbot"
        st.rerun()

# -------------------- STEP: CHATBOT --------------------
elif st.session_state.step == "chatbot":
    st.title(f"💬 Chat with ARYA")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": f"Hi {st.session_state.name}! What would you like to discuss about your quiz?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about your performance..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("ARYA is thinking..."):
                evaluator = Evaluator(topic=st.session_state.topic, paper=st.session_state.result['paper'])
                response = evaluator.chat(prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response}) 