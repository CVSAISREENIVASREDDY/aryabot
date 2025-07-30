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
cd aryabot 
```
### 2. Create and Activate a Virtual Environment

* **For Windows**:

    ```bash
    python -m venv venv
    .\\venv\\Scripts\\activate
    ```

* **For macOS/Linux**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 3. Install Dependencies

Install all the required packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Set Up Your Environment Variables

Create a `.env` file in the root of the project and add your Google API key like this:


## How to Run ධ
Once you have completed the setup, you can run the application with the following command:
GOOGLE_API_KEY="YOUR_API_KEY"

```bash
streamlit run app.py
```