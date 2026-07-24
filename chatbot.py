import pandas as pd
from groq import Groq
import os
from dotenv import load_dotenv

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


    data_summary = f"""

    Dataset columns:
    {list(df.columns)}

    Total records:
    {len(df)}

    Sample data:
    {df.head(5).to_string()}

    """


    prompt = f"""

    You are a startup funding data analyst.

    Use only the dataset information below.

    {data_summary}


    User question:
    {question}


    Give a clear answer.
    If the answer is not available in the dataset,
    say "No data available".

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