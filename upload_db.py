import pandas as pd
from sqlalchemy import create_engine
from db_connect import get_connection
import streamlit as st


# Load cleaned dataset
df = pd.read_csv("data/cleaned_startup_funding.csv")

print("Dataset loaded")
print(df.head())
print("Rows and Columns:", df.shape)


# Create database engine

engine = create_engine(
    f"postgresql://{st.secrets['DB_USER']}:{st.secrets['DB_PASSWORD']}@"
    f"{st.secrets['DB_HOST']}:{st.secrets['DB_PORT']}/"
    f"{st.secrets['DB_NAME']}"
)


# Upload to PostgreSQL

try:
    df.to_sql(
        "startup_funding_data",
        engine,
        if_exists="replace",
        index=False
    )

    print("✅ Cleaned dataset uploaded successfully!")

except Exception as e:
    print("❌ Upload error:", e)