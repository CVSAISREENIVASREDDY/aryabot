# ARYA AI Interview Prep ✨

ARYA is an interactive, AI-powered application designed to help users prepare for technical interviews. By leveraging Google's Gemini model, ARYA dynamically generates questions, evaluates answers in real-time, and provides personalized feedback to help you improve.


## Features 🚀

* **Dynamic Question Generation**: Get unique quiz questions for any technical topic you want to practice.
* **Variable Difficulty**: Questions are generated for **Easy**, **Medium**, and **Hard** difficulty levels to test your knowledge comprehensively.
* **Timed Environment**: Each question is timed (30s, 45s, 60s) to simulate the pressure of a real interview.
* **AI-Powered Evaluation**: Your answers are evaluated by ARYA using a weighted scoring system (Easy: 30%, Medium: 40%, Hard: 30%) to provide a final score.
* **Personalized Feedback**: Receive a concise, actionable suggestion from ARYA to help you improve on the topic.
* **Interactive Chatbot**: After the quiz, you can chat with ARYA to discuss your answers and get further clarification.

---

## Tech Stack 🛠️

* **Language**: Python
* **Framework**: Streamlit
* **AI Model**: Google Gemini 1.5 Flash
* **Libraries**: `google-generativeai`, `python-dotenv`

---

## Setup and Installation ⚙️

Follow these steps to get ARYA running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/CVSAISREENIVASREDDY/aryabot.git 

# For Windows
python -m venv venv
.\\venv\\Scripts\\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

streamlit run app.py

