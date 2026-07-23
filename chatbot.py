import ollama

def ai_chatbot(df, question):

    # Dataset Summary
    summary = f"""
Total Records: {len(df)}

Columns:
{', '.join(df.columns)}

Numeric Summary:
{df.describe(include='number').to_string()}

Categorical Summary:
{df.describe(include='object').to_string()}

Top 20 Sample Rows:
{df.head(20).to_string(index=False)}
"""

    prompt = f"""
You are an expert Startup Funding Data Analyst.

Below is information about a startup funding dataset.

{summary}

User Question:
{question}

Instructions:
- Answer only using the dataset information.
- Give numerical insights whenever possible.
- Keep the answer clear and professional.
- If the dataset does not contain the requested information, say so.
"""

    # Show prompt in terminal
    print("\n" + "=" * 80)
    print("PROMPT SENT TO OLLAMA")
    print("=" * 80)
    print(prompt)

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]

    # Show response in terminal
    print("\n" + "=" * 80)
    print("OLLAMA RESPONSE")
    print("=" * 80)
    print(answer)

    return answer