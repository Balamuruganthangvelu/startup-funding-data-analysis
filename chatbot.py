import streamlit as st
from groq import Groq


# ---------------- GROQ CLIENT ----------------

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


# ---------------- CHATBOT FUNCTION ----------------

def chatbot(df, question):

    # Check data
    if df is None or df.empty:
        return "No data available for analysis."


    # Dataset information
    columns = list(df.columns)

    rows = len(df)


    # Create dataset summary

    try:
        statistics = df.describe(
            include="all"
        ).to_string()

    except Exception:
        statistics = "Statistics not available"


    sample = df.head(5).to_string()



    context = f"""
    You are an expert data analyst.
    Analyze only the given dataset.
    Dataset Information:
    Number of rows:
    {rows}
    Columns:
    {columns}
    
    Statistical Summary:
    {statistics}
    
    Sample Records:
    {sample}
"""
    prompt = f"""
    You are a startup funding data analyst.
    You have a dataset with this information:
    {context}
    
    Answer the user's question directly.
    Rules:
    - Do NOT write Python code.
    - Do NOT show SQL queries.
    - Do NOT create a dataframe.
    - Do NOT explain programming steps.
    - Give only the final business answer.
    - Include numbers and insights from the dataset.
    - Use simple sentences.
    
    User Question:
    {question}
"""
    try:

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )


        return response.choices[0].message.content



    except Exception as e:

        return f"AI Error: {e}"