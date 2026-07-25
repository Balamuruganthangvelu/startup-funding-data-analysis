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

{context}


User Question:

{question}


Instructions:

- Answer based only on the dataset.
- If calculation is required, explain the calculation.
- Provide clear business insights.
- Do not say you cannot access the data.
- If the answer is not available in the dataset, say:
  "This information is not available in the dataset."


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