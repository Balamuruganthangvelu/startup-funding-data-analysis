import pandas as pd
from groq import Groq
import os
from dotenv import load_dotenv
from intent import detect_intent
from data_analyzer import analyze

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def chatbot(df, question):

    question_lower = question.lower()


    # ---------------- GENERAL KNOWLEDGE QUESTIONS ----------------

    general_questions = [
        "what is startup funding",
        "explain startup funding",
        "what is venture capital",
        "what is investor",
        "what is startup"
    ]


    if any(q in question_lower for q in general_questions):

        prompt = f"""
        Answer this question in a simple way:

        Question:
        {question}

        Explain for a beginner.
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content



    # ---------------- DATASET ANALYSIS ----------------


    if df is None or df.empty:
        return "No data available."

    intent = detect_intent(question)

    if intent != "llm":
        result = analyze(df, intent)

        if result is None:
            return "No data available."
        prompt = f"""
        You are an AI assistant for a startup funding dashboard.
        Convert the following analysis result into a natural answer.
        
        Result:
        {result}
        
        Rules:
        - Answer directly.
        - Do not generate SQL.
        - Do not generate Python.
        - Do not explain your reasoning.
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content
    return "No data available."