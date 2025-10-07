import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
LLM_MODEL = "gemini-2.5-flash"
genai.configure(api_key=api_key)

class Questioner:
    def __init__(self, topic: str,  n: int):
        self.topic = topic
        self.n = n
        system_ins = f"""You are an expert in {topic} and you are interviewing a person in the field of {topic}.
        When the user asks you to give easy questions - you have to give them {n} beginner level questions in a JSON array format.
        Similarly for medium and hard also, you have to give only {n} questions based on the difficulty level.
        The {n} questions should be from diverse topics.
        ask 1 question them to code also but the expected answer to the coding question should be a one-liner.
        You can ask any questions from the topic but the expected answer should not exceed more than 10 words.
        Give only questions, no answers, no annotations, no documentation, just {n} concise questions.
        Format your output as a valid JSON array of strings like ["Q1", "Q2", "Q3"].
        Only return the JSON array. No explanation.
        IMPORTANT: Make sure all of the {n} questions are completely related to {topic}. 
        """
        self.model = genai.GenerativeModel(LLM_MODEL, system_instruction=system_ins)

    def generate(self, level):
        response = self.model.generate_content(level)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[len("```json"):].strip()
        elif text.startswith("```"):
            text = text[len("```"):].strip()
        if text.endswith("```"):
            text = text[:-3].strip()
        try:
            questions = json.loads(text)
            if isinstance(questions, list):
                return questions
            else:
                return []
        except json.JSONDecodeError:
            return []

class Evaluator:
    def __init__(self, topic: str, paper: dict):
        self.topic = topic
        self.paper = paper
        self.model = genai.GenerativeModel(LLM_MODEL)

    def evaluate(self):
        scores = {"easy": [], "medium": [], "hard": []}
        
        for qa in self.paper["qa"]:
            level = qa["level"]
            # A more direct prompt to get just a score
            prompt = f"On a scale of 0 to 10, rate the correctness of the answer for the following question. Respond with only a single integer.\n\nQuestion: {qa['question']}\nAnswer: {qa['answer']}"
            
            try:
                response = self.model.generate_content(prompt)
                # Use regex to find any number in the response text
                score_match = re.search(r'\d+', response.text)
                if score_match:
                    score = int(score_match.group(0))
                    scores[level].append(score)
                else:
                    scores[level].append(0) # Append 0 if no number is found
            except Exception:
                scores[level].append(0)

        # Calculate weighted score
        easy_avg = sum(scores["easy"]) / len(scores["easy"]) if scores["easy"] else 0
        medium_avg = sum(scores["medium"]) / len(scores["medium"]) if scores["medium"] else 0
        hard_avg = sum(scores["hard"]) / len(scores["hard"]) if scores["hard"] else 0

        # Apply weights: 30% easy, 40% medium, 30% hard
        total_score = (easy_avg * 0.3) + (medium_avg * 0.4) + (hard_avg * 0.3)
        
        # Get overall suggestion
        qa_text = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}" for qa in self.paper["qa"]])
        suggestion_prompt = f"""You are an expert evaluator. Based on the following Q&A, provide one simple, clear, and constructive suggestion to help the user improve.\n\n{qa_text}"""
        
        suggestion = "Could not generate a suggestion."
        try:
            suggestion_response = self.model.generate_content(suggestion_prompt)
            suggestion = suggestion_response.text.strip()
        except Exception:
            pass

        return {
            "score": round(total_score * 10),  # Scale score to be out of 100
            "suggestion": suggestion,
            "paper": self.paper
        }
        
    def chat(self, user_prompt:str):
        # The paper is now nested inside the result object from evaluate()
        paper_details = json.dumps(self.paper, indent=2)
        prompt = f"""You are a helpful AI assistant. A user has just completed a quiz on the topic of '{self.topic}'.
        Here is their performance data:
        If user asks questions out of context, politely inform them that you can only discuss their quiz performance. 
        
        {paper_details}
        
        The user asks: "{user_prompt}"
        
        Provide a helpful and encouraging response based on their quiz performance data."""
        
        response = self.model.generate_content(prompt)
        return response.text.strip()

if __name__ == "__main__" :
    q = Questioner("python",2) 
    responses = q.generate("easy")
    print(responses)
