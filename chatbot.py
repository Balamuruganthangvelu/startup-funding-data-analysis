import os
import json
import ollama

from groq import Groq
from dotenv import load_dotenv

from prompts import INTENT_PROMPT
from executor import execute_plan


load_dotenv()


AI_PROVIDER = os.getenv(
    "AI_PROVIDER",
    "ollama"
)


groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



# ---------------- SCHEMA CREATION ----------------

def get_schema(df):

    schema = {}

    for col in df.columns:

        samples = (
            df[col]
            .dropna()
            .head(3)
            .tolist()
        )


        samples = [
            str(value)
            for value in samples
        ]


        schema[col] = {

            "dtype": str(df[col].dtype),

            "sample_values": samples

        }


    return schema




# ---------------- ASK AI ----------------

def ask_ai(prompt):


    if AI_PROVIDER == "ollama":


        response = ollama.chat(

            model="llama3.1:8b",

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }

            ]

        )


        return response["message"]["content"]



    elif AI_PROVIDER == "groq":


        response = groq_client.chat.completions.create(


            model="llama-3.1-8b-instant",


            messages=[

                {
                    "role": "system",
                    "content": "Return only valid JSON"
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ]

        )


        return response.choices[0].message.content






# ---------------- MAIN CHATBOT ----------------

def chatbot(df, question):


    # 1. Create schema

    schema = get_schema(df)



    # 2. Create planner prompt

    intent_prompt = INTENT_PROMPT.format(

        schema=json.dumps(
            schema,
            indent=2,
            default=str
        ),

        question=question

    )



    # 3. Ask AI for plan

    plan_response = ask_ai(
        intent_prompt
    )



    # 4. Extract JSON

    try:

        clean_response = (

            plan_response
            .replace("```json", "")
            .replace("```", "")
            .strip()

        )


        start = clean_response.find("{")

        end = clean_response.rfind("}") + 1


        plan = json.loads(

            clean_response[start:end]

        )


    except Exception:


        return (
            "I could not understand the question."
        )



    # 5. Execute pandas operation

    result = execute_plan(

        df,

        plan

    )



    # 6. No data found

    if not result["success"]:

        return (
            "I couldn't find an answer "
            "to that question in the uploaded dataset."
        )



    data = result["result"]



    # ---------------- FORMAT RESPONSE ----------------



    # Columns answer

    if isinstance(data, dict):


        if "total_columns" in data:


            return (

                f"The dataset contains "
                f"{data['total_columns']} columns.\n\n"

                "Columns:\n"

                + ", ".join(
                    data["columns"]
                )

            )



        # Summary answer only when user asks summary

        if "mean" in data:


            return (

                "Here is the dataset summary:\n\n"

                f"Total: ₹ {data['sum']:,.0f}\n"

                f"Average: ₹ {data['mean']:,.0f}\n"

                f"Minimum: ₹ {data['min']:,.0f}\n"

                f"Maximum: ₹ {data['max']:,.0f}\n"

                f"Records: {data['count']}"

            )



    # List result

    if isinstance(data, list):


        if len(data) == 0:

            return (
                "Nothing to show."
            )


        answer_prompt = f"""

You are a data analyst.

User question:
{question}


Dataset result:

{json.dumps(data, indent=2, default=str)}


Rules:

- Answer only from the dataset result.
- Do not use outside knowledge.
- Do not summarize unrelated information.
- If the result does not answer the question, say:

"I couldn't find an answer to that question in the uploaded dataset."

Give a short plain English answer.

"""


        return ask_ai(answer_prompt)




    return str(data)